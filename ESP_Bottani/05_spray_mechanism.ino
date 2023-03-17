int z_value = 0;
int x_value = 0;
int s_value = 0;
void sampling_spray(){
  z_value = 0;
  x_value = 0;
  s_value = 0;
  if(button_s_up){
    z_value = 1;
  }
  else if(button_s_down){
    z_value = -1;
  }
  if(button_s_right){
    x_value = 1;
  }
  else if(button_s_left){
    x_value = -1;
  }
  if(button_s_spray){
    s_value = 1;
  }
  runmotor(Z,PWM_Z*z_value);
  runmotor(X,PWM_X*x_value);
  digitalWrite(PUMP,s_value);
}
