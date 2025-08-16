#include"pid.h"

void pid_init(PID_Controller *pid, float Kp, float Ki, float Kd, float output_min, float output_max)
{
    pid->Kp = Kp;
    pid->Ki = Ki;
    pid->Kd = Kd;
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->output_min = output_min;
    pid->output_max = output_max;
}


float pid_compute(PID_Controller *pid, float setpoint, float measured_value, float dt)
{
    float error = setpoint - measured_value;
    pid->integral += error * dt;

    float derivative = (error - pid->prev_error) / dt;
    float output = pid->Kp * error + pid->Ki * pid->integral + pid->Kd * derivative;

    // Clamp output
    if (output > pid->output_max) output = pid->output_max;
    else if (output < pid->output_min) output = pid->output_min;

    pid->prev_error = error;
    return output;
}
