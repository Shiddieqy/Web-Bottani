void setup(){
  Serial.begin(115200);
  wifi_setup();
  firebase_setup();
  ledcSetup(L, PWM_FREQUENCY , PWM_RES);
  ledcAttachPin(L_PWM, L);

  ledcSetup(R, PWM_FREQUENCY , PWM_RES);
  ledcAttachPin(R_PWM, R);

  ledcSetup(X, PWM_FREQUENCY , PWM_RES);
  ledcAttachPin(X_PWM, X);

  ledcSetup(Z, PWM_FREQUENCY , PWM_RES);
  ledcAttachPin(Z_PWM, Z);

  pinMode(L_FORWARD,OUTPUT);
  pinMode(L_REVERSE,OUTPUT);
  pinMode(R_FORWARD,OUTPUT);
  pinMode(R_REVERSE,OUTPUT);
  pinMode(X_FORWARD,OUTPUT);
  pinMode(X_REVERSE,OUTPUT);
  pinMode(Z_FORWARD,OUTPUT);
  pinMode(Z_REVERSE,OUTPUT);
  pinMode(PUMP,OUTPUT);
}
