
void loop(){
  if((millis()-button_timer)>ts_button){
    button_timer = millis();
      parse_button();
      sampling_track();
      sampling_spray();
  }
  if ((millis()-sensor_timer)>ts_sensor){
    sensor_timer = millis();
    sampling_sensor();
  }

}
