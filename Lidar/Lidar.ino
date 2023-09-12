#include "LidarMaster.h"
#include "StepperMaster.h"
#include "Gimbal.h"
#include <WiFi.h>

const char* ssid = "CarcamoBorges";
const char* password = "2NT1@lw3FC4";
const uint16_t port = 8090;
const char* host = "192.168.1.185";


StepperMaster stepperOne(16, 17, 18, 19);
StepperMaster stepperTwo(27, 26, 25, 33);
Gimbal gimbal(&stepperOne, &stepperTwo, 900);
LidarMaster lidar(0x10);




void setup()
{
  pinMode(13, INPUT); //Data ready pin
  Serial.begin(115200);
  xTaskCreatePinnedToCore(Core0LidarSend, "CPU_0", 10000, NULL, 0, NULL, 0); //create task on second core

  //Gimbal setup
  Serial.println("Centralizando Gimbal...");
  gimbal.returnToHome();
  Serial.println("Pronto.");
  delay(1000);
  stepperOne.sequence(LOW, LOW, LOW, LOW); //if lidar isnt in action relief stress on stepper
  stepperTwo.sequence(LOW, LOW, LOW, LOW);

  //WiFi Setup
  Serial.print("Conectando a rede "); Serial.println(ssid);
  delay(2000);

  WiFi.begin(ssid, password);
  int retryIntervalMs = 500;
  int timeoutCounter = 20;
  while (WiFi.status() != WL_CONNECTED) //wait for WiFi connection
  {
    delay(retryIntervalMs);
    if (timeoutCounter == 0)
    {
      WiFi.reconnect();
      timeoutCounter = 20;
      //Serial.println("\nConnection to WiFi failed trying again... ");
    }
    timeoutCounter--;
  }

  Serial.print("\nConectado na rede com o IP: ");
  Serial.println(WiFi.localIP());

}


WiFiClient client;

bool searching = true;
bool trigger = false;


void loop() {


  if (searching) Serial.println("Buscando por host..."); //only coninue if python socket host was found
  if (!client.connect(host, port)) {
    searching = false;
    delay(1000);
    return;
  }


  searching = true;
  Serial.println("Host encontrado!");

  Serial.print("Temperatura do Lidar: "); Serial.print(lidar.getTemperatur()); Serial.println("°");
  trigger = true;
  scanVertical(50, 10, -15, 40, 15, 1);
  Serial.println("Scan concluído. Disconectando do host...");
  client.stop();
  delay(5000);
  gimbal.rotateTo(0, 0, 20);
  delay(1000);
  stepperOne.sequence(LOW, LOW, LOW, LOW);
  stepperTwo.sequence(LOW, LOW, LOW, LOW);

}


void Core0LidarSend(void * parameter) {
  sendLidarDataContinous();
}

void sendLidarDataContinous() {
  String package;
  uint16_t dist;
  uint16_t strength;
  double lastH = stepperOne.getAbsoluteAngle();
  double lastV = stepperTwo.getAbsoluteAngle();
  int interval = 100;
  int count = 0;
  bool readReady = false;

  while (true) { //infinity loop
    while (trigger) { //only send data while scan is active
      readReady = digitalRead(13);  //wait for data ready signal to avoid false lidar read outs
      if (newData(lastH, lastV) && readReady) { //newData determines the resolution i.e. every n° new data is send
        dist = lidar.getDistance();
        strength = lidar.getAmp();
        if (dist < 12000 && strength < 30000) {
          package = String(stepperOne.getAbsoluteAngle()) + "," + String(stepperTwo.getAbsoluteAngle()) + "," + String(dist) + "," + String(strength) + "|";
          client.print(package); //send data
          count ++; //count data points
        }
      }
      vTaskDelay(5); //lidar refresh rate is 250Hz meaning every 4ms there is new data
    }
    if (count > 0) {
      Serial.print("Scan finalizado. "); Serial.print(count); Serial.println(" datapoints foram mapeados!");
      count = 0;
    }
    vTaskDelay(50);
  }
}

bool newData(double &lastH, double &lastV) {
  double resolution = 0.5;
  if (abs(lastH - stepperOne.getAbsoluteAngle()) > resolution || abs(lastV - stepperTwo.getAbsoluteAngle()) > resolution) {
    lastH = stepperOne.getAbsoluteAngle();
    lastV = stepperTwo.getAbsoluteAngle();
    return true;
  } else {
    return false;
  }
}

void scanHorizontal(int hStart, int vStart, int row, int angleSpeed, int stepDist) {
  Serial.println("Escaneando linha horizontal...");
  trigger = true;
  int v = vStart;
  int h = hStart;
  while (h > hStart - row) {
    gimbal.rotateTo(h, v, angleSpeed);
    h --;
    gimbal.rotateTo(h, v, angleSpeed);
    v *= (-1);
  }
  trigger = false;
}

void scanVertical(int amplitude, int hStart, int vStart, int cols, int angleSpeed, int stepDist) {
  Serial.println("Escaneando linha vertical...");
  trigger = true;
  int v = vStart;
  int h = hStart;
  while (v < vStart + cols) {
    gimbal.rotateTo(h, v, angleSpeed);
    amplitude *= (-1);
    h = h + amplitude;
    gimbal.rotateTo(h, v, angleSpeed);
    v += stepDist;
  }
  trigger = false;
}


void scanCircle(int r, int zero, int stepDistance) {
  double x, y, i;
  for (i = 0; i < 360; i += stepDistance) {
    y = r * cos((PI / 180.0) * i) + zero;
    x = r * sin((PI / 180.0) * i) + zero;
    gimbal.rotateTo(y, x, 70);
  }
}
