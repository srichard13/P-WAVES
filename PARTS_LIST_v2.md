# P-WAVES parts list

This parts list documents the major hardware used in the P-WAVES experiments and notes the recommended configuration for a new build. It is intended to accompany the P-WAVES manuscript and public control-code repository.

## Major components used in the study

| Component | Manufacturer / model | Qty. | Function / important specification | Approx. unit cost (USD) |
|---|---|---:|---|---:|
| Wet-stream mass-flow controller | Alicat Scientific **MC-200SCCM-D-DB9M/5M**, gas: Air | 1 | Controls flow through the moisture exchanger. Nominal 200 sccm full scale. This legacy unit was used because it was already available. | Legacy unit; not used for current-build cost estimate |
| Dry-stream mass-flow controller | Alicat BASIS **BC-500C-N2V25A-00LV03** | 1 | Controls dry dilution flow; nominal 500 sccm full scale. | ~400-500 |
| Moisture exchanger | Perma Pure **BE-060-24COMP2-SS** | 1 | 24 in BE-series exchanger, 0.063 in O.D.; submerged in the water bath to humidify the wet branch. | **233** (purchase price) |
| Water reservoir / bath | ~400 mL glass Mason jar with custom 3D-printed lid insert | 1 | Holds distilled/deionized water. Lid insert accommodates 1/8 in compression bulkhead fittings for the Perma Pure exchanger tubing. | Low-cost / custom |
| 3-way solenoid valve | Parker Series 9 **091-0094-900** | 1 | 12 VDC, 3-way valve; 1/8 in FNPT ports; vacuum to 100 psig. | Vendor dependent |
| 2-way solenoid valve | Clippard **ES-2W-12-L** | 1 | 12 VDC, 2-way bidirectional solenoid valve used for automated gas routing. | ~50 |
| Solid-state relay | Sensata / Crydom **D1D07** | 2 | DC solid-state relays used to switch valve power in the final configuration. | ~55-80 each |
| Control computer | **Raspberry Pi** single-board computer | 1 | Runs the Python P-WAVES control program and communicates with analyzer/control hardware. Exact Pi model is not critical to the method. | ~50-85 |
| Analog / digital interface | Pi-Plates **DAQC2plate** | 1 | Provides DAC outputs for MFC commands and digital outputs for valve control. Maximum DAC output is ~4.095 V. | ~60 |
| Power supply | TRACO Power **TPP 65-321M2** | 1 | 65 W multi-output AC/DC supply; 12 VDC, 5 VDC, and -12 VDC rails. | ~110-120 |
| Gas tubing | **1/8 in stainless-steel tubing** | Assorted | Wetted gas plumbing. | Varies |
| Compression fittings | **Swagelok 1/8 in compression fittings**, tees, unions, and bulkheads | Assorted | Used throughout the stainless-steel gas path. | Varies |
| Clippard valve adapter | Non-Swagelok brass adapter / fitting | 1 set | Adapts the Clippard valve to the 1/8 in stainless-steel tubing. Manufacturer/model not established. | Low |
| Wiring / connectors | Hook-up wire, terminal blocks, serial/USB cabling, connectors | Assorted | Electrical interconnection and analyzer communication. | ~25-75 |
| Portable enclosure | General-purpose portable enclosure | 1 | Houses the P-WAVES flow and control components. Exact enclosure is intentionally unspecified because the redesigned system fits in a smaller enclosure than the experimental case. | Application dependent |

**Cost note.** Costs are approximate representative prices where available and should not be interpreted as exact historical purchase prices. The Perma Pure price is the documented purchase price. Based on the recommended current-build configuration (including two lower-cost 500 sccm BASIS-series MFCs), a reasonable approximate total component cost is **~$2,000 USD**, excluding the calibration gas cylinder/regulator, the analyzer under test, temporary diagnostic flow meters, and external display/computer equipment. The total is intentionally approximate because fitting, enclosure, and vendor pricing can vary substantially.

## Recommended configuration for a new build

The experimental system used a 200 sccm wet-stream MFC because that controller was already available. For a new build, use **500 sccm lower-cost BASIS-series MFCs on both the wet and dry branches**.

The DAQC2 output used by P-WAVES is limited to about 4.095 V while the Alicat analog command is scaled to 5 V full scale. The effective maximum commanded flow is therefore approximately 82% of the nominal MFC rating:

- nominal 200 sccm MFC -> ~164 sccm effective maximum;
- nominal 500 sccm MFC -> ~410 sccm effective maximum.

A 500 sccm wet-side controller therefore provides sufficient capacity to generate a fully humidified stream at the ~250 sccm flow required by the Picarro analyzers. The older 200 sccm MC-series controller was larger and more expensive than necessary and is not recommended for a new build.

## Design-history and test-configuration notes

- An additional 200 sccm MFC was present in the original P-WAVES design but was removed during redesign because its function was no longer required.
- Additional Alicat flow meters were temporarily installed during diagnostic and validation experiments to verify actual gas flows. These diagnostic meters are not part of the field-deployable P-WAVES system and are not included in the parts list above. Their temporary use added wetted volume and surface area during those experiments.
- Earlier versions used **KG-1D-V4-50 inline solenoid-valve driver boards**, labeled as 50% duty-cycle drivers, to reduce valve power consumption and heat generation. Following a reliability problem with one of these modules, the final configuration used two Crydom D1D07 solid-state relays.
- Most experiments reported in the manuscript used the ~400 mL Mason-jar water bath. A low-cost vacuum-insulated vessel was substituted during later reviewer-response testing to evaluate thermal effects on generated H2O stability; it is not required for basic P-WAVES operation.
- The gas path used 1/8 in stainless-steel tubing and Swagelok compression fittings throughout, except for the Clippard-valve connection, which required a non-Swagelok adapter.
