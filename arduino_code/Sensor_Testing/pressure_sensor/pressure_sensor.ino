int AnalogPin1 = 0; // FSR is connected to analog 0
int AnalogPin2 = 1;
int fsrReading1;
int fsrReading2;
int fsrReading;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);  
pinMode(AnalogPin1, INPUT);
pinMode(AnalogPin2, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  fsrReading1 = analogRead(AnalogPin1);
  fsrReading2 = analogRead(AnalogPin2);
  fsrReading = round((fsrReading1+fsrReading2));
  Serial.println(fsrReading);
  delay(100);
}
