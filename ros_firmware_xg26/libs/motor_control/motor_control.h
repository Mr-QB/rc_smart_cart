#ifndef LIBS_MOTOR_CONTROL_MOTOR_CONTROL_H_
#define LIBS_MOTOR_CONTROL_MOTOR_CONTROL_H_
#define PWM_FREQ 1000
#define INITIAL_DUTY_CYCLE 0
#define PWM1_PORT gpioPortD
#define PWM1_PIN  8
#define LPWM1_PORT gpioPortB
#define LPWM1_PIN  7
#define RPWM1_PORT gpioPortB
#define RPWM1_PIN  8
#define PWM2_PORT gpioPortD
#define PWM2_PIN  9
#define LPWM2_PORT gpioPortC
#define LPWM2_PIN  5
#define RPWM2_PORT gpioPortC
#define RPWM2_PIN  4


#include "em_gpio.h"
#include <math.h>

#include "em_timer.h"
#include "em_cmu.h"
#include "em_gpio.h"
#include "em_timer.h"
#include "pid.h"
#include "../encoder/encoder.h"
#include "../uart/uart.h"

void initCMU(void);
void initGPIO(void);
void initTIMER(void);

void motor1_forward(void);
void motor1_backward(void);
void motor2_forward(void);
void motor2_backward(void);
void motor_control_update(void);
void motor1_set_target_speed(float speed_mps);
void motor2_set_target_speed(float speed_mps);
void motor_control_init(void);
void read_wheel_velocity(void);
float get_motor1_set_target_speed(void);
float get_motor2_set_target_speed(void);

extern volatile float dutyCycle1;
extern volatile float dutyCycle2;



#endif /* LIBS_MOTOR_CONTROL_MOTOR_CONTROL_H_ */
