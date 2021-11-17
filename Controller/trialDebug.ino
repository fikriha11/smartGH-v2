

void debug() {
  if (Serial.available()) {
    SerialData = Serial.readString();
    for (int a = 0; a < SerialData.length(); a++) {
      Data[a] = GetData(SerialData, ',', a);
    }
  }
}

String GetData(String data, char Spliter, int Number) {
  StringData = 0;
  SplitData = "";

  for (int i = 0; i < data.length(); i++) {
    if (data[i] == Spliter) {
      StringData++;
    }
    else if (StringData == Number) {
      SplitData.concat(data[i]);
    }
    else if (StringData > Number) {
      return SplitData;
      break;
    }
  }
  return SplitData;
}
