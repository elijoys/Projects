# Dual EMG Asymmetry Meter

An Arduino-based prototype that measures left- and right-leg electromyography (EMG) signals during Nordic hamstring curl repetitions, calculates RMS signal amplitude for each channel, and displays an LSI-style symmetry estimate on a 16×2 LCD.

> **Disclaimer:** This is an experimental measurement prototype, not a medical device. EMG amplitude is not a direct measurement of muscle force, and the displayed LSI-style value is not a clinical assessment of ACL recovery or return-to-sport readiness.

## Overview

The system collects EMG signals from both legs and compares their amplitudes over a short recording window. After each repetition, it displays a Limb Symmetry Index (LSI)-style percentage and a complementary asymmetry percentage.

### Processing pipeline

1. **Baseline calibration** — averages each EMG channel while both legs are relaxed for approximately two seconds.
2. **Countdown** — displays a 3–2–1 countdown before each repetition.
3. **Signal acquisition** — records 1,024 samples per channel at a target sampling frequency of 1,000 Hz.
4. **Baseline correction** — subtracts each channel's resting average from its samples.
5. **RMS calculation** — calculates the root mean square (RMS) amplitude for each channel.
6. **Symmetry calculation** — compares the lower and higher RMS values.
7. **LCD output** — displays LSI-style symmetry and asymmetry percentages, then starts a rest period before the next repetition.

## Hardware

- Arduino board with 12-bit ADC support (the sketch uses `analogReadResolution(12)`)
- Two EMG sensor modules, one for each leg
- 16×2 character LCD compatible with the Arduino `LiquidCrystal` library
- Jumper wires and suitable power connections
- Electrodes and sensor interfaces appropriate for the selected EMG modules

### Pin assignments

| Component | Arduino pin |
|---|---|
| Left EMG signal | `A0` |
| Right EMG signal | `A1` |
| LCD RS | `12` |
| LCD Enable | `11` |
| LCD D4 | `5` |
| LCD D5 | `4` |
| LCD D6 | `3` |
| LCD D7 | `2` |

The LCD is initialized with:

```cpp
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
```

**Hardware note:** Confirm your specific board's ADC resolution, reference voltage, and input limits before wiring. The sketch assumes a 0–3.3 V, 12-bit ADC when converting counts to millivolts. Do not connect an EMG output that exceeds the board's permitted input range.

## Software requirements

Install these Arduino libraries through the Arduino IDE Library Manager:

- **LiquidCrystal** — character LCD control (often included with the Arduino AVR core)
- **arduinoFFT** — included in the sketch for possible future frequency-domain analysis

The current sketch computes RMS amplitude directly. Although the FFT library, objects, and sample buffers are initialized, **no FFT is executed in the current processing loop**.

## Measurement and calculations

### RMS amplitude

For a baseline-corrected signal containing \(N\) samples, RMS is calculated as:

\[
x_{\mathrm{RMS}} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}x_i^2}
\]

The sketch converts RMS counts to an estimated millivolt value using:

```cpp
rms_mV = rmsCounts * (3300.0 / 4095.0);
```

This conversion assumes a 3.3 V ADC reference and 12-bit readings. It represents an ADC-equivalent voltage estimate; the actual EMG voltage depends on the sensor's amplification and signal-conditioning circuitry.

### LSI-style symmetry and asymmetry

The sketch currently uses the same generic comparison for both sides:

\[
\mathrm{LSI} = \frac{\min(L,R)}{\max(L,R)} \times 100
\]

\[
\mathrm{Asymmetry} = 100 - \mathrm{LSI}
\]

Here, \(L\) and \(R\) are the left and right EMG RMS-derived metrics.

**Example:** If the left RMS value is 0.80 mV and the right is 0.60 mV, the LSI-style result is 75% and the asymmetry result is 25%.

The current `emgToMetric()` function simply returns its input. It does **not** convert EMG amplitude to force or strength. The code also does not identify which side is injured; it compares whichever value is lower with whichever is higher.

## Typical operating cycle

- **Startup:** LCD initialization and approximately two seconds of relaxed baseline collection.
- **Countdown:** 3 seconds.
- **Recording:** 1,024 samples per channel at a target of 1,000 Hz (nominally 1.024 seconds).
- **Result:** LSI-style and asymmetry percentages displayed for 5 seconds.
- **Rest:** 3 seconds before the next countdown.

The sampling loop uses software timing and sequential analog reads. Actual sample timing should be verified on the target hardware if precise timing is important.

## Getting started

1. Wire the LCD and two EMG signal outputs according to the pin table.
2. Verify the sensor outputs are compatible with the board's ADC input range.
3. Install the required Arduino libraries.
4. Open the project sketch in the Arduino IDE and select the correct board and port.
5. Upload the sketch.
6. At startup, keep both legs relaxed during baseline calibration.
7. Follow the countdown and perform a Nordic hamstring curl when prompted.
8. Read the displayed values after each recording window.

For consistent experiments, keep electrode placement, sensor gain, posture, movement technique, and measurement conditions as consistent as possible.

## Current limitations

- EMG RMS amplitude is not a direct measure of muscle force or strength.
- The placeholder metric conversion performs no calibration.
- There is no injured/uninjured limb configuration.
- The full recording window is analyzed; the code does not segment the eccentric phase or detect repetition boundaries from the signal.
- EMG is not normalized to a reference contraction.
- The baseline is measured once at startup and is not updated during use.
- FFT functionality is included but unused.
- The current code does not store measurements for later review or trend analysis.
- If both metrics are zero, the code leaves LSI and asymmetry at zero, which should be treated as an uninformative result rather than a valid symmetry assessment.

## Potential future improvements

- Add data logging over serial or save results to a file.
- Validate the sample rate and consider hardware-timed acquisition.
- Add signal-quality checks and handling for disconnected or saturated sensors.
- Detect and segment each repetition and its eccentric phase.
- Add reference-contraction normalization and document the protocol.
- Track left and right values across repetitions and sessions.
- Use a validated strength or functional test alongside EMG before making rehabilitation-related interpretations.
- Implement FFT-based frequency metrics if they support a clearly defined project goal.

## Safety and intended use

This project is intended for educational experimentation with embedded systems and EMG signal processing. It is not intended to diagnose an injury, prescribe rehabilitation, or determine readiness to return to sport. Follow the EMG hardware manufacturer's instructions, use appropriate electrical isolation and power practices, and consult a qualified clinician for ACL rehabilitation decisions.
