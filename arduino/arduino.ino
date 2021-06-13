String morse_codes[] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.", "-----", "......", ".-.-.-", "--..--", "..--..", "-.-.-.", "---..."};
char* symbols[] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", ",", "!", "?", ";", ":", " "};

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

#define button_pin A3
#define dynamic_pin 11

boolean button_flag = 0;      // Флаг для определения наличия сигнала от кнопки
boolean time_word_flag = 0;
boolean time_letter_flag = 0;

// ОТСЧЕТ ВРЕМЕНИ ВЕДЕТСЯ С НАЧАЛА ЗАПУСКА ПРОГРАММЫ ( функция millis() )
unsigned long pressed_time;  // Переменная для хранения времени для определения времени зажатой кнопки
unsigned long released_time; // Переменная для хранения времени для определения времени не зажатой кнопки
unsigned long sound_time;    // Переменная для хранения времени для определения длительности сигнала

String userInput = "";       // Переменная хранящая строку ввода пользователя
String mode_flag = "m_to_l"; // Флаг для переключения между режимами: "a_to_l", "l_to_a" (по умолчанию "a_to_l")

int j = 0;

int count_sym_1 = 0;     // Переменная для переключения по столбцам дисплея
boolean count_sym_2 = 0; // Переменная для перемещения по строкам дисплея

void setup() {
  pinMode(button_pin, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  lcd.init();                     
  lcd.backlight();

  Serial.begin(9600);
}

void loop() {
  boolean button_flag = 0;
  boolean time_word_flag = 0;
  time_letter_flag = 0;    

  userInput = "";  

  int j = 0;

  int count_sym_1 = 0; 
  boolean count_sym_2 = 0;

  // С Азбуки Морзе в Латиницу
  while (mode_flag == "m_to_l"){
    from_morse();
  }

  // С Латиницы в Азбуку Морзе
  while (mode_flag == "l_to_m"){
    to_morse();
  }
}

void to_morse(){
  userInput = "SOS";
  int j = 0;
  if (userInput == "m_to_l"){
    mode_flag = "m_to_l";
  }
  else{
    while (userInput[j] != '\0'){
      int index = 0;
      for (int i = 0; i <= 42; i++){
        if ((String)userInput[j] == symbols[i]){
          index = i;
          break;
        }
      }
      int k = 0;
      while (morse_codes[index][k] != '\0'){
        if (morse_codes[index][k] == '-'){
          Serial.println("-");
          sound_time = millis();
          while (millis() - sound_time < 550){
            analogWrite(dynamic_pin, 10);
          }
          sound_time = millis();
          while (millis() - sound_time < 100){
            analogWrite(dynamic_pin, 0);
          }
        }
        else if (morse_codes[index][k] == '.'){
          Serial.println(".");
          sound_time = millis();
          while (millis() - sound_time < 150){
            analogWrite(dynamic_pin, 10);
          }
          sound_time = millis();
          while (millis() - sound_time < 100){
            analogWrite(dynamic_pin, 0);
          }
        }
        k++;
      }
      j++;
      delay(900);
    }
    delay(1800);
  }
  mode_flag = "m_to_l";
}

void from_morse() {
  boolean button = !digitalRead(button_pin);
  
  if (button == true && button_flag == 0){
    digitalWrite(13, HIGH);
    analogWrite(dynamic_pin, 10);
    pressed_time = millis();
    button_flag = !button_flag;
  }
  else if (button != true && button_flag != 0) {
    if (millis() - pressed_time >= 300){
      userInput = userInput + "-";
    }
    else if (millis() - pressed_time < 300){
      userInput = userInput + ".";
    }
    digitalWrite(13, LOW);
    analogWrite(dynamic_pin, 0);
    button_flag = !button_flag;
    released_time = millis();
    time_word_flag = 1;
    time_letter_flag = 1;
  }
  if (button != true && millis() - released_time > 800 && time_letter_flag != 0){
    lcd.setCursor(count_sym_1, count_sym_2);
    int index = 0;
    for (int i = 0; i <= 42; i++){
      if (userInput == morse_codes[i]){
        index = i;
        break;
      }
    }

    Serial.println(symbols[index]);
    lcd.print(symbols[index]);
    count_sym_1++;
    if (count_sym_1 > 15 && count_sym_2 == 0){
      count_sym_1 = 0;
      count_sym_2 = 1;
    }
    else if (count_sym_1 > 15 && count_sym_2 == 1){
      count_sym_1 = 0;
      count_sym_2 = 0;
      lcd.clear();
    }      
    userInput = "";
      
    time_letter_flag = 0;
  }
  if (button != true && millis() - released_time >= 2000 && time_word_flag != 0){
    lcd.setCursor(count_sym_1, count_sym_2);
    Serial.println(" ");
    lcd.print(symbols[42]);
    count_sym_1++;
    if (count_sym_1 > 15 && count_sym_2 == 0){
      count_sym_1 = 0;
      count_sym_2 = 1;
    }
    else if (count_sym_1 > 15 && count_sym_2 == 1){
      count_sym_1 = 0;
      count_sym_2 = 0;
      lcd.clear();
    }

    time_word_flag = 0;
  }
  if (Serial.available() > 0) {
    userInput = Serial.readString();
    if (userInput == "InErr"){
      //lcd.clear();
      lcd.setCursor(--count_sym_1, count_sym_2);
      lcd.print(userInput);
      delay(1500);
      lcd.setCursor(--count_sym_1, count_sym_2);
      lcd.print("      ");
      userInput = "";
    }
    else if (userInput == "l_to_m"){
      mode_flag = "l_to_m";
    }
  }
}