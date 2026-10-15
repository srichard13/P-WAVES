
import piplates.DAQC2plate as DAQC2
import time
import math
from datetime import datetime
import serial
import os

# ===== ANSI COLOR CODES =====
BOLD = "\033[1m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

board = 0
wet_port = 1
dry_port = 0
gas_sol = 0
wet_shunt = 1

MIN_TOTAL_FLOW = 0.0  # Aeris can run at lower total flows
CONDITIONING_WET_FLOW = 5.0  # ccm wet air shunted to room for BE/Nafion conditioning

WET_MFC_FULL_SCALE = 200.0
DRY_MFC_FULL_SCALE = 500.0
DAC_MAX = 4.095
ALICAT_FULL_SCALE_V = 5.0

wet_effective_fs = WET_MFC_FULL_SCALE * (DAC_MAX / ALICAT_FULL_SCALE_V)
dry_effective_fs = DRY_MFC_FULL_SCALE * (DAC_MAX / ALICAT_FULL_SCALE_V)

def safe_float(prompt, default):
    value = input(prompt)
    try:
        return float(value) if value else default
    except ValueError:
        return default

def safe_int(prompt, default):
    value = input(prompt)
    try:
        return int(value) if value else default
    except ValueError:
        return default

def F_to_C(Tf):
    return (Tf - 32.0) * 5.0 / 9.0

def saturation_ppm(Tc):
    Psat_kPa = 0.61078 * math.exp((17.27 * Tc) / (Tc + 237.3))
    Patm_kPa = 101.325
    return (Psat_kPa / Patm_kPa) * 1e6

print("\n=== Humidity Step Controller - AERIS ===\n")

mode = input("Run mode? (q=quick, f=full) [f]: ").strip().lower()
quick = (mode == "q")

instrument_sn = input("Enter instrument SN (default AERIS_798): ").strip() or "AERIS_798"
operator = input("Operator (optional): ").strip()
notes = input("Notes (optional): ").strip()

default_predry = 60.0 if quick else 120.0
default_num_steps = 6 if quick else 20
default_step_time = 60 if quick else 180

predry_time = safe_float(f"Enter pre-dry time (default {default_predry:.0f} s): ", default_predry)
total_flow = safe_float("Enter total flow (default 300 sccm): ", 300.0)

if total_flow < MIN_TOTAL_FLOW:
    print("WARNING: Total flow raised to 260 sccm minimum.")
    total_flow = MIN_TOTAL_FLOW

num_steps = safe_int(f"Enter number of steps (default {default_num_steps}): ", default_num_steps)
step_time = safe_int(f"Enter step time in seconds (default {default_step_time}): ", default_step_time)

Tf = safe_float("Enter bath temp (default 70 F): ", 70.0)
Tc = F_to_C(Tf)
sat = saturation_ppm(Tc)

start_ppm = safe_float("Enter starting ppm (default 0): ", 0.0)
max_ppm_possible_at_total_flow = sat * (wet_effective_fs / total_flow)
end_ppm = safe_float(f"Enter ending ppm (default max achievable ≈ {max_ppm_possible_at_total_flow:.0f} ppm at {total_flow:.0f} sccm): ", max_ppm_possible_at_total_flow)

step_increment = (end_ppm - start_ppm) / (num_steps - 1)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
time.sleep(2)

ser.reset_input_buffer()
time.sleep(0.2)
ser.reset_input_buffer()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"humidity_step_aeris_{timestamp}.csv"
f = open(filename, "w")

# ---- Metadata header (comment lines starting with '#') ----
run_mode = "quick" if quick else "full"
max_ppm_possible = sat * (wet_effective_fs / total_flow)

f.write("# Humidity step test data\n")
f.write(f"# Timestamp: {timestamp}\n")
f.write(f"# Script Version: {os.path.basename(__file__)}\n")
f.write(f"# Run_mode: {run_mode}\n")
f.write(f"# Instrument_SN: {instrument_sn}\n")
f.write(f"# Operator: {operator}\n")
f.write(f"# Notes: {notes}\n")
f.write(f"# Predry_time_s: {predry_time}\n")
f.write(f"# Total_flow_sccm: {total_flow}\n")
f.write(f"# Num_steps: {num_steps}\n")
f.write(f"# Step_time_s: {step_time}\n")
f.write(f"# Bath_temp_F: {Tf}\n")
f.write(f"# Bath_temp_C: {Tc}\n")
f.write(f"# Saturation_ppm: {sat}\n")
f.write(f"# Start_ppm: {start_ppm}\n")
f.write(f"# End_ppm: {end_ppm}\n")
f.write(f"# Step_increment_ppm: {step_increment}\n")
f.write(f"# Conditioning_wet_flow_sccm: {CONDITIONING_WET_FLOW}\n")
f.write(f"# Wet_MFC_full_scale_sccm: {WET_MFC_FULL_SCALE}\n")
f.write(f"# Dry_MFC_full_scale_sccm: {DRY_MFC_FULL_SCALE}\n")
f.write(f"# DAC_max_V: {DAC_MAX}\n")
f.write(f"# Alicat_full_scale_V: {ALICAT_FULL_SCALE_V}\n")
f.write(f"# Wet_effective_fs_sccm: {wet_effective_fs}\n")
f.write(f"# Dry_effective_fs_sccm: {dry_effective_fs}\n")
f.write(f"# Max_ppm_possible_at_total_flow: {max_ppm_possible}\n")
f.write("# ---- Data columns ----\n")

f.write("Year,Month,Day,Hour,Minute,Second,Step,"
        "Wet_sccm,Dry_sccm,Target_ppm,"
        "P_mbar,T0_C,T2_C,Tgas_C,"
        "CH4_wet_ppm,CH4_ppm,H2O_ppm,"
        "C2H6_wet_ppb,C2H6_ppb,TEC_Power_W\n")

DAQC2.setDOUTbit(board, gas_sol)
time.sleep(1)

DAQC2.setDOUTbit(board, wet_shunt)
print(f"Pre-dry started (duration {predry_time:.0f} s)...")
start_time = time.time()

while (time.time() - start_time) < predry_time:
    DAQC2.setDAC(board, wet_port, min((CONDITIONING_WET_FLOW / wet_effective_fs) * DAC_MAX, DAC_MAX))
    DAQC2.setDAC(board, dry_port, min((total_flow / dry_effective_fs) * DAC_MAX, DAC_MAX))
    time.sleep(1)

step = 0
last_step_time = time.time()

while step < num_steps:

    now = datetime.now()

    target_ppm = start_ppm + step * step_increment

    # O1 (wet_shunt) control:
    # ON during 0-ppm generation (and OFF otherwise) to keep BE/Nafion conditioned
    if target_ppm <= 0.0:
        DAQC2.setDOUTbit(board, wet_shunt)
    else:
        DAQC2.clrDOUTbit(board, wet_shunt)
    # Limit target_ppm to what the wet MFC can actually deliver at the DAQC2 max DAC voltage.
    # This preserves constant total_flow (dry + wet) and prevents the instrument from drawing room air.
    max_ppm = sat * (wet_effective_fs / total_flow)
    if target_ppm > max_ppm:
        print(f"WARNING: Requested target {target_ppm:.0f} ppm exceeds max achievable {max_ppm:.0f} ppm at total_flow={total_flow:.0f} sccm (wet max ~{wet_effective_fs:.1f} sccm). Capping.")
        target_ppm = max_ppm


    if target_ppm <= 0.0:
        wet_flow = CONDITIONING_WET_FLOW
        dry_flow = total_flow
    else:
        wet_flow = total_flow * (target_ppm / sat)
        dry_flow = total_flow - wet_flow

    wet_v = min((wet_flow / wet_effective_fs) * DAC_MAX, DAC_MAX)
    dry_v = min((dry_flow / dry_effective_fs) * DAC_MAX, DAC_MAX)

    DAQC2.setDAC(board, wet_port, wet_v)
    DAQC2.setDAC(board, dry_port, dry_v)

    # ---- Read one Aeris data line (CSV) ----
    latest = None

    while ser.in_waiting:

        latest = ser.readline().decode('utf-8', errors='ignore').strip()


    if latest is None:

        latest = ser.readline().decode('utf-8', errors='ignore').strip()


    line = latest

    fields = line.split(',')
    if len(fields) > 46:
        # ---- Extract Aeris fields ----
        P_mbar = float(fields[2])
        T0_C = float(fields[3])
        T2_C = float(fields[5])
        Tgas_C = float(fields[7])

        ch4_wet = float(fields[34])
        ch4_dry = float(fields[35])
        h2o_ppm = float(fields[36])
        c2h6_wet = float(fields[37])
        c2h6_dry = float(fields[38])
        tec_power = float(fields[45])

        row = (
            f"{now.year},{now.month:02d},{now.day:02d},"
            f"{now.hour:02d},{now.minute:02d},{now.second:02d},"
            f"{step+1},{wet_flow:.3f},{dry_flow:.3f},{target_ppm:.2f},"
            f"{P_mbar},{T0_C},{T2_C},{Tgas_C},"
            f"{ch4_wet},{ch4_dry},{h2o_ppm},"
            f"{c2h6_wet},{c2h6_dry},{tec_power}\n"
        )

        f.write(row)

        print(
            f"{BOLD}{now.hour:02d}:{now.minute:02d}:{now.second:02d}{RESET} | "
            f"{MAGENTA}{BOLD}STEP {step+1}/{num_steps}{RESET} | "
            f"Target={target_ppm:.0f} ppm | "
            f"{BLUE}{BOLD}H2O={h2o_ppm:.0f} ppm{RESET} | "
            f"{GREEN}CH4={ch4_dry:.3f}{RESET} | "
            f"{CYAN}C2H6={c2h6_dry:.3f}{RESET}"
        )

    if (time.time() - last_step_time) >= step_time:
        step += 1
        if step < num_steps:
            print(f"{YELLOW}{BOLD}=== ADVANCING TO NEXT STEP {step+1}/{num_steps} ==={RESET}")
        last_step_time = time.time()

    time.sleep(1)

f.close()
ser.close()

DAQC2.setDAC(board, wet_port, 0)
DAQC2.setDAC(board, dry_port, 0)
DAQC2.clrDOUTbit(board, gas_sol)
DAQC2.clrDOUTbit(board, wet_shunt)

print("Run complete. Flows set to zero. Solenoid closed.")
