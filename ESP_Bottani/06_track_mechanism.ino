int left_value = 0;
int right_value = 0;

void runtrack(int left,int right){
  runmotor(L,PWM_L*left);
  runmotor(R,PWM_R*right);
}
void sampling_track(){
  left_value = 0;
  right_value = 0;
  if(button_up){
    left_value += 1;
    right_value += 1;
  }
   if(button_down){
    left_value -= 1;
    right_value -= 1;
  }
    if(button_left){
    left_value += 1;
    right_value -= 1;
  }
    if(button_right){
    left_value -= 1;
    right_value += 1;
  }
    Serial.print(btn);
  Serial.print("\t");
    Serial.print(button_up);
  Serial.print("\t");
    Serial.print(button_down);
  Serial.print("\t");
    Serial.print(button_right);
  Serial.print("\t");
    Serial.print(button_left);
  Serial.print("\t");
  Serial.print(left_value);
  Serial.print("\t");
  Serial.println(right_value);
  runtrack(left_value,right_value);
}
