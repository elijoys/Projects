/****************************************************
*Dual EMG Asymmetry Meter (Nordic Rep, LSI-style)
****************************************************/


// Install Libraries
#include <LiquidCrystal.h>   // 16x2 LCD
#include <arduinoFFT.h>      // Fast-Fourier Transform
#include <math.h>           


// LCD wiring
// LiquidCrystal(rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


//EMG input pins
const int EMG_L_PIN = A0;    // LEFT EMG
const int EMG_R_PIN = A1;    // RIGHT EMG


// Sampling/FFT
// ~1 second rep window: 1024 samples at 1000 Hz
const uint16_t N_SAMPLES = 1024;          // samples per block (power of 2)
const double   FS_HZ     = 1000.0;        // sampling frequency (Hz)
const unsigned long TS_US = (unsigned long)(1000000.0 / FS_HZ); // sample period (µs)


// Arrays for FFT Data
// LEFT channel
double vRealL[N_SAMPLES];
double vImagL[N_SAMPLES];
// RIGHT channel
double vRealR[N_SAMPLES];
double vImagR[N_SAMPLES];


// --- FFT objects (ready for later if you want frequency metrics) ---
ArduinoFFT<double> FFT_L = ArduinoFFT<double>(vRealL, vImagL, N_SAMPLES, FS_HZ);
ArduinoFFT<double> FFT_R = ArduinoFFT<double>(vRealR, vImagR, N_SAMPLES, FS_HZ);


// Baseline (DC offset) for each channel
float baselineL = 0.0;
float baselineR = 0.0;


// ---------------------------------------------------------
// SETUP: ADC + LCD + 2 s baseline calibration
// ---------------------------------------------------------
void setup() {
 analogReadResolution(12);  // 12-bit: 0–4095


 // 2) LCD initiation
 lcd.begin(16, 2);
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print(" Dual EMG Initiation ");
 lcd.setCursor(0, 1);
 lcd.print("Relax both legs");
 delay(1000);


 // 3) Baseline calibration (~2 s, relaxed)
 unsigned long startCal = millis();
 long sumL = 0;
 long sumR = 0;
 long count = 0;


 while (millis() - startCal < 2000) {   // 2 seconds
   int rawL = analogRead(EMG_L_PIN);
   int rawR = analogRead(EMG_R_PIN);


   sumL += rawL;
   sumR += rawR;
   count++;
 }


 // 4) Average baselines
 if (count > 0) {
   baselineL = (float)sumL / (float)count;
   baselineR = (float)sumR / (float)count;
 } else {
   baselineL = 0.0;
   baselineR = 0.0;
 }


 // 5) Show baselines briefly
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("BaseL:");
 lcd.print(baselineL, 0);
 lcd.setCursor(0, 1);
 lcd.print("BaseR:");
 lcd.print(baselineR, 0);
 delay(1000);
}




// ---------------------------------------------------------
// Collect samples from both EMGs
// ---------------------------------------------------------
void acquireBlock(double &sumSqL, double &sumSqR, int &count) {
 sumSqL = 0.0;
 sumSqR = 0.0;
 count  = 0;


 unsigned long t0 = micros();


 for (uint16_t i = 0; i < N_SAMPLES; i++) {
   // Wait until it's time for this sample
   unsigned long targetTime = t0 + TS_US * (unsigned long)(i + 1);
   while (micros() < targetTime) {
     // busy-wait
   }


   // Read EMG from both channels
   int rawL = analogRead(EMG_L_PIN);
   int rawR = analogRead(EMG_R_PIN);


   // Remove baseline (center signal)
   double centeredL = (double)rawL - baselineL;
   double centeredR = (double)rawR - baselineR;


   // Store for FFT
   vRealL[i] = centeredL;
   vImagL[i] = 0.0;
   vRealR[i] = centeredR;
   vImagR[i] = 0.0;


   // Accumulate squares for RMS
   sumSqL += centeredL * centeredL;
   sumSqR += centeredR * centeredR;
   count++;
 }
}




// ---------------------------------------------------------
// Convert sum of squares -> RMS voltage in mV
// ---------------------------------------------------------
float countsToRMSmV(double sumSq, int count) {
 if (count <= 0) return 0.0;


 double meanSq    = sumSq / (double)count;
 double rmsCounts = sqrt(meanSq);


 // Due: 0–4095 counts => 0–3300 mV
 float rms_mV = (float)(rmsCounts * (3300.0 / 4095.0));
 return rms_mV;
}




// ---------------------------------------------------------
// Placeholder calibration: EMG RMS (mV) -> "metric"
// Later: replace with your EMG->force equation
// ---------------------------------------------------------
float emgToMetric(float rms_mV) {
 return rms_mV;
}




// ---------------------------------------------------------
// Show a 3-2-1 countdown before each Nordic rep
// ---------------------------------------------------------
void showCountdown() {
 for (int sec = 3; sec > 0; sec--) {
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print("Get ready in");
   lcd.setCursor(0, 1);
   lcd.print(sec);
   lcd.print("...");
   delay(1000);  // wait 1 second
 }


 // Brief "GO" screen before recording starts
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("DO NORDIC NOW");
 lcd.setCursor(0, 1);
 lcd.print("Recording...");
 // No delay here: acquireBlock() will start immediately after
}




// ---------------------------------------------------------
// LOOP: countdown -> record one rep (~1 s) -> compute
//       RMS, LSI, asymmetry -> show result -> rest -> repeat
// ---------------------------------------------------------
void loop() {
 // 1) Countdown before the rep
 showCountdown();


 // 2) Record one rep (~1 second window)
 double sumSqL, sumSqR;
 int    nSamples;
 acquireBlock(sumSqL, sumSqR, nSamples);  // blocking for ~1 s


 // 3) Compute RMS in mV for each limb
 float rmsL_mV = countsToRMSmV(sumSqL, nSamples);
 float rmsR_mV = countsToRMSmV(sumSqR, nSamples);


 // 4) Convert RMS -> metric (e.g., "force" later)
 float metricL = emgToMetric(rmsL_mV);
 float metricR = emgToMetric(rmsR_mV);


 // 5) Compute LSI and Asymmetry (%)
 float weaker   = min(metricL, metricR);
 float stronger = max(metricL, metricR);


 float LSI = 0.0;          // Limb Symmetry Index (%)
 float asymPercent = 0.0;  // 100 - LSI


 if (stronger > 0.0f) {
   LSI = (weaker / stronger) * 100.0f;  // LSI = weaker/stronger * 100
   asymPercent = 100.0f - LSI;          // Asymmetry = 100 - LSI
 }


 // 6) Show results on LCD
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("LSI:");
 lcd.print(LSI, 1);
 lcd.print("%");


 lcd.setCursor(0, 1);
 lcd.print("Asym:");
 lcd.print(asymPercent, 1);
 lcd.print("%");


 // Hold the result so you can read/discuss
 delay(5000);   // 5 seconds


 // 7) Optional short rest between reps
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("Rest...");
 delay(3000);   // 3 seconds rest


 // Then loop() repeats: countdown -> next rep -> new result
}
