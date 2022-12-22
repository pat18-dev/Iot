//thanks to @tolribeiro
//http://toribeiro.com/articles/2016-01/sound-level-meter-using-esp8266-arduino-sound-detector
//for inspiration here particularly around calculating dBs
//#include <LiquidCrystal.h>

const float dBAnalogQuiet = 10; // calibrated value from analog input (48 dB equivalent)
const float dBAnalogMedium = 12;
const float dBAnalogLoud = 17;

//LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

#define PIN_ANALOG_IN A0

void setup()
{

  //lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(A2, INPUT);
}

void loop()
{
  int value;
  float decibelsValueQuiet = 49;
  float decibelsValueMedium = 65;
  float decibelsValueLoud = 70;

  value = analogRead(PIN_ANALOG_IN);

  if (value < 13)
  {
    decibelsValueQuiet += 20 * log10(value/dBAnalogQuiet);
    Serial.println(value);
    printDecibels("Quiet :)", decibelsValueQuiet);
    }
  else if ((value > 13) && ( value <= 23) )
  {
    decibelsValueMedium += log10(value/dBAnalogMedium);
        Serial.println(value);
    printDecibels("Medium", decibelsValueMedium);
  }
  else if(value > 22)
  {
    decibelsValueLoud += log10(value/dBAnalogLoud);
        Serial.println(value);
    printDecibels("Loud :(", decibelsValueLoud);
  }
  delay(500);
}

void printDecibels (const char* volume, float dBs)
{
  //lcd.clear();
  //lcd.setCursor(0,0);
  
  Serial.print(volume);
  //lcd.setCursor(0,1);
  Serial.print(" : ");
  Serial.print(dBs);
  Serial.println(" dB");
}