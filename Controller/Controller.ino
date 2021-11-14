
#define Pump 1
#define MotorMixA 2
#define MotorMixB 3
#define MotorMixCampuran 7
#define ValveMixA 4
#define ValveMixB 5
#define VTCampuran 8


#define ON  1
#define OFF 2

int interval = 1000;
int vTandonUtama = 0;
int vTandonCampuran = 0;
int flowMixA = 0;
int flowMixB = 0;
float konstanta = 4.5;

bool ProsesMixing = false;
bool IsiTandonCampuran = false;
bool PenambahanABmix = false;
bool Distribusi = false;
bool Mixing = false;

bool PupukA = false;
bool PupukB = false;


struct SensorFlow {
  int Count;
  int Calc;
} FlowA, FlowB;



void BacaSensorTandonUtama() {
  vTandonUtama = analogRead(A2);
  if (vTandonUtama < 200) {
    ProsesMixing = true;
    IsiTandonCampuran = true;
  }
}

bool WaterLvlTandonCampuran() {
  vTandonCampuran = analogRead(A3);
  if (vTandonCampuran > 5000) {
    return false;
  } else {
    return true;
  }
}

void Pompa(int Status) {
  if (Status == ON) {
    digitalWrite(Pump, HIGH);
  } else {
    digitalWrite(Pump, LOW);
  }
}

void MotorMix(int Type, int Status) { 
  if (Status == ON) {
    digitalWrite(Type, HIGH);
  } else {
    digitalWrite(Type, LOW);
  }
}

int FlowMeterA() {
  unsigned long ltime = millis();
  unsigned long Volume = 0;
  if ((millis() - ltime) >= interval) {
    detachInterrupt(0);
    float debit = float((interval / (millis() - ltime)) *  FlowA.Count) / konstanta;
    ltime = millis();
    int flowmlt = (debit / 60.0) * interval;
    Volume += flowmlt;
    FlowA.Count = 0;
    attachInterrupt(00, pulseCounterA, RISING);
    return Volume;
  }
}

int FlowMeterB() {
  unsigned long ltime = millis();
  unsigned long Volume = 0;
  if ((millis() - ltime) >= interval) {
    detachInterrupt(0);
    float debit = float((interval / (millis() - ltime)) *  FlowB.Count) / konstanta;
    ltime = millis();
    int flowmlt = (debit / 60.0) * interval;
    Volume += flowmlt;
    FlowB.Count = 0;
    attachInterrupt(00, pulseCounterB, RISING);
    return Volume;
  }
}



void setup() {
  Serial.begin(9600);
  attachInterrupt(00, pulseCounterA, RISING);
  attachInterrupt(00, pulseCounterB, RISING);
}


void loop() {
  if (ProsesMixing) {

    /******* Isi Air Tandon Campuran ******/
    if (IsiTandonCampuran) {
      if (WaterLvlTandonCampuran()) {
        Pompa(ON);
        MotorMix(MotorMixA, ON);
        MotorMix(MotorMixB, ON);
      } else {
        Pompa(OFF);
        MotorMix(MotorMixA, OFF);
        MotorMix(MotorMixB, OFF);
        IsiTandonCampuran = false;
        PenambahanABmix = true;
        PupukA = true;
      }
    }

    /******* Proses Penambahan Pupuk ABmix ******/
    else if (PenambahanABmix) {
      if (PupukA) {
        digitalWrite(ValveMixA, HIGH);
        if (FlowMeterA() >= 500) {
          digitalWrite(ValveMixA, LOW);
          PupukA = false;
          PupukB = true;
        }
      } else if (PupukB) {
        digitalWrite(ValveMixB, HIGH);
        if (FlowMeterA() >= 500) {
          digitalWrite(ValveMixB, LOW);
          PupukB = false;
          Mixing = true;
          PenambahanABmix = false;
        }
      }
    }

    /******* Proses Mixing tandon Campuran ******/
    else if (Mixing) {
      MotorMix(MotorMixCampuran, ON);
      delay(50000);
      MotorMix(MotorMixCampuran, OFF);
      Mixing = false;
      Distribusi = true;
    }

    /******* Proses Distribusi Pupuk ******/
    else if (Distribusi) {
      digitalWrite(VTCampuran, HIGH);
      if (!WaterLvlTandonCampuran()) {
        digitalWrite(VTCampuran, LOW);
        ProsesMixing = false;
      }
    }
  }
}

void pulseCounterA() {
  FlowA.Count++;
}

void pulseCounterB() {
  FlowB.Count++;
}
