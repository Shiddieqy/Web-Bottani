enum Motor{L,R,X,Z};
int pwm[N_Motor] = {L_PWM,R_PWM,X_PWM,Z_PWM};
int forward[N_Motor] = {26,R_FORWARD,X_FORWARD,Z_FORWARD};
int m_reverse[N_Motor] = {27,R_REVERSE,X_REVERSE,Z_REVERSE};

void runmotor(int channel,int cmd){
  ledcWrite(channel, abs(cmd));
  if (cmd>0){
    digitalWrite(forward[channel],HIGH);
    digitalWrite(m_reverse[channel],LOW);
  }
  else{
    digitalWrite(forward[channel],LOW);
    digitalWrite(m_reverse[channel],HIGH);
  }
}
