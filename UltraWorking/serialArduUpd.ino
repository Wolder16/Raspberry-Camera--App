// аналог пины
#define POT 0
#define THERM 1
#define PHOTO 2
#define JOYX 6
#define JOYY 7

// дигит пины
#define MNP1_PIN 9
#define MNP2_PIN 5
#define MNP3_PIN 6


#include <Servo.h>
Servo mnp1;
Servo mnp2;
Servo mnp3;




// 0x27 или 0x3f





#include "EncButton.h"
#include "Parser.h"
#include "AsyncStream.h"  // асинхронное чтение сериал
AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ

EncButton<EB_TICK, BTN> btn;
bool flag = 0;

void setup() {
  Serial.begin(115200);
  mnp1.attach(MNP1_PIN);
  mnp2.attach(MNP2_PIN);
  mnp3.attach(MNP3_PIN);
  pinMode(13, 1);
  pinMode(LED_R, 1);
  pinMode(LED_G, 1);
  pinMode(LED_B, 1);
  pinMode(MOS, 1);
  pinMode(RELAY, 1);
}

// с ардуино на пк, терминтаор \n
// 0,потенц,фоторез,термистор
// 1,кнопка
// 2,joyx,joyy

// с пк на ардуино, терминтаор ;
// 0,лед 13
// 1,r,g,b
// 2,angle
// 3,fan
// 4,relay
// 5,text

void loop() {
  parsing();

  btn.tick();
  static uint32_t tmr = 0;
  if (millis() - tmr > 100) {
    tmr = millis();
    Serial.print(0);
    Serial.print(',');
    Serial.print(analogRead(POT));
    Serial.print(',');
    Serial.print(analogRead(PHOTO));
    Serial.print(',');
    Serial.println(therm.getTempAverage(), 2);
  }

  static uint32_t tmr2 = 0;
  if (millis() - tmr2 > 50) {
    tmr2 = millis();
    Serial.print(2);
    Serial.print(',');
    Serial.print(analogRead(JOYX));
    Serial.print(',');
    Serial.println(analogRead(JOYY));
  }

  if (btn.isClick()) {
    flag = !flag;
    Serial.print(1);
    Serial.print(',');
    Serial.println(flag);
  }
}

// функция парсинга, опрашивать в лупе
void parsing() {
  if (serial.available()) {
    Parser data(serial.buf, ',');  // отдаём парсеру
    int ints[10];           // массив для численных данных
    data.parseInts(ints);   // парсим в него

    switch (ints[0]) {
      case 0: digitalWrite(13, ints[1]);
        break;
      case 1:
        mnp1.write(0);
        break;
      case 2:
        mnp1.write(90)
        break;
      case 3:
        mnp2.write(0)
        break;
      case 4:
        mnp2.write(90)
        break;
      case 5:
        mnp3.write(0)
        break;
      case 6:
        mnp3.write(90)
        break;

      


    }
  }
}
