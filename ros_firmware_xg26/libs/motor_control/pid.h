/*
 * pid.h
 *
 *  Created on: Aug 8, 2025
 *      Author: cai
 */

#ifndef LIBS_MOTOR_CONTROL_PID_H_
#define LIBS_MOTOR_CONTROL_PID_H_

typedef struct {
    float Kp;
    float Ki;
    float Kd;
    float setpoint;
    float integral;
    float prev_error;
    float output_min;
    float output_max;
} PID_Controller;

void pid_init(PID_Controller *pid, float Kp, float Ki, float Kd, float output_min, float output_max);
float pid_compute(PID_Controller *pid, float setpoint, float measured_value, float dt);


#endif /* LIBS_MOTOR_CONTROL_PID_H_ */
