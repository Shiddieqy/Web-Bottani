
float temperature;
float humidity;
float moisture;

void sampling_sensor(){
  temperature = 20.5+random(1,100)*1.0/20;
  humidity = 20.5+random(1,100)*1.0/20;
  moisture = 20.5+random(1,100)*1.0/20;
  publish_float(temperature,T_TOPIC);
  publish_float(humidity,H_TOPIC);
  publish_float(moisture,M_TOPIC);
}
