//#include "pid_position.h"
//
//// PID hệ vị trí cho encoder
//static float Kp = 1.5f;
//static float Ki = 0.0003f;//0.005f;
//static float Kd = 0.04f;//0.04f;
//
//static float prev_error = 0;
//static float integral = 0;
//
//void pid_position_init(float kp, float ki, float kd) {
//  Kp = kp;
//  Ki = ki;
//  Kd = kd;
//  pid_position_reset();
//}
//
//void pid_position_reset(void) {
//  prev_error = 0;
//  integral = 0;
//}
//
//float pid_position_compute(int32_t target, int32_t current) {
//  float error = (float)(target - current);
//  integral += error;
//  float derivative = error - prev_error;
//  prev_error = error;
//
//  float output = Kp * error + Ki * integral + Kd * derivative;
//  return output;
//}
