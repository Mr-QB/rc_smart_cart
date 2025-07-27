#ifndef MOTOR_PWM_H
#define MOTOR_PWM_H


#include "em_gpio.h"
#include "em_timer.h"

// Khai báo các hàm khởi tạo
void initCMU(void);
void initGPIO(void);
void initTIMER(void);

// Điều khiển động cơ
void motor1_forward(void);
void motor1_backward(void);
void motor2_forward(void);
void motor2_backward(void);

// Biến điều chỉnh duty cycle
extern volatile float dutyCycle1;
extern volatile float dutyCycle2;

#endif // MOTOR_H
