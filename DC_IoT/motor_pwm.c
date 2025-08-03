//#include "motor_pwm.h"
//#include "em_cmu.h"
//#include "em_gpio.h"
//#include "em_timer.h"
//
//#define PWM_FREQ             1000
//#define INITIAL_DUTY_CYCLE   0//50
//
//// Motor 1
//#define PWM1_PORT  gpioPortD
//#define PWM1_PIN   8
//#define LPWM1_PORT gpioPortB
//#define LPWM1_PIN  7
//#define RPWM1_PORT gpioPortB
//#define RPWM1_PIN  8
//
//// Motor 2
//#define PWM2_PORT  gpioPortD
//#define PWM2_PIN   9
//#define LPWM2_PORT gpioPortC
//#define LPWM2_PIN  5
//#define RPWM2_PORT gpioPortC
//#define RPWM2_PIN  4
//
//volatile float dutyCycle1 = INITIAL_DUTY_CYCLE;
//volatile float dutyCycle2 = INITIAL_DUTY_CYCLE;
//
//void initCMU(void) {
//  CMU_ClockEnable(cmuClock_GPIO, true);
//  CMU_ClockEnable(cmuClock_TIMER0, true);
//}
//
//void initGPIO(void) {
//  GPIO_PinModeSet(PWM1_PORT, PWM1_PIN, gpioModePushPull, 0);
//  GPIO_PinModeSet(LPWM1_PORT, LPWM1_PIN, gpioModePushPull, 0);
//  GPIO_PinModeSet(RPWM1_PORT, RPWM1_PIN, gpioModePushPull, 0);
//  GPIO_PinModeSet(PWM2_PORT, PWM2_PIN, gpioModePushPull, 0);
//  GPIO_PinModeSet(LPWM2_PORT, LPWM2_PIN, gpioModePushPull, 0);
//  GPIO_PinModeSet(RPWM2_PORT, RPWM2_PIN, gpioModePushPull, 0);
//}
//
//void initTIMER(void) {
//  TIMER_Init_TypeDef timerInit = TIMER_INIT_DEFAULT;
//  TIMER_InitCC_TypeDef ccInit = TIMER_INITCC_DEFAULT;
//
//  timerInit.enable = false;
//  ccInit.mode = timerCCModePWM;
//
//  TIMER_Init(TIMER0, &timerInit);
//
//  GPIO->TIMERROUTE[0].ROUTEEN = GPIO_TIMER_ROUTEEN_CC0PEN | GPIO_TIMER_ROUTEEN_CC1PEN;
//  GPIO->TIMERROUTE[0].CC0ROUTE = (PWM1_PORT << _GPIO_TIMER_CC0ROUTE_PORT_SHIFT)
//                               | (PWM1_PIN << _GPIO_TIMER_CC0ROUTE_PIN_SHIFT);
//  GPIO->TIMERROUTE[0].CC1ROUTE = (PWM2_PORT << _GPIO_TIMER_CC1ROUTE_PORT_SHIFT)
//                               | (PWM2_PIN << _GPIO_TIMER_CC1ROUTE_PIN_SHIFT);
//
//  TIMER_InitCC(TIMER0, 0, &ccInit);
//  TIMER_InitCC(TIMER0, 1, &ccInit);
//
//  uint32_t top = CMU_ClockFreqGet(cmuClock_TIMER0) / PWM_FREQ;
//  TIMER_TopSet(TIMER0, top);
//
//  TIMER_CompareSet(TIMER0, 0, (top * dutyCycle1) / 100);
//  TIMER_CompareSet(TIMER0, 1, (top * dutyCycle2) / 100);
//
//  TIMER_Enable(TIMER0, true);
//}
//
//void motor1_forward(void) {
//  GPIO_PinOutSet(LPWM1_PORT, LPWM1_PIN);
//  GPIO_PinOutClear(RPWM1_PORT, RPWM1_PIN);
//}
//void motor1_backward(void) {
//  GPIO_PinOutClear(LPWM1_PORT, LPWM1_PIN);
//  GPIO_PinOutSet(RPWM1_PORT, RPWM1_PIN);
//}
//void motor2_forward(void) {
//  GPIO_PinOutSet(LPWM2_PORT, LPWM2_PIN);
//  GPIO_PinOutClear(RPWM2_PORT, RPWM2_PIN);
//}
//void motor2_backward(void) {
//  GPIO_PinOutClear(LPWM2_PORT, LPWM2_PIN);
//  GPIO_PinOutSet(RPWM2_PORT, RPWM2_PIN);
//}


#include "motor_pwm.h"
#include "em_cmu.h"
#include "em_gpio.h"
#include "em_timer.h"
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
volatile float dutyCycle1 = INITIAL_DUTY_CYCLE;
volatile float dutyCycle2 = INITIAL_DUTY_CYCLE;
void initCMU(void) { CMU_ClockEnable(cmuClock_GPIO, true); CMU_ClockEnable(cmuClock_TIMER0, true); }
void initGPIO(void) {
  GPIO_PinModeSet(PWM1_PORT, PWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(LPWM1_PORT, LPWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(RPWM1_PORT, RPWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(PWM2_PORT, PWM2_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(LPWM2_PORT, LPWM2_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(RPWM2_PORT, RPWM2_PIN, gpioModePushPull, 0);
}
void initTIMER(void) {
  TIMER_Init_TypeDef timerInit = TIMER_INIT_DEFAULT;
  TIMER_InitCC_TypeDef ccInit = TIMER_INITCC_DEFAULT;
  timerInit.enable = false;
  ccInit.mode = timerCCModePWM;
  TIMER_Init(TIMER0, &timerInit);
  GPIO->TIMERROUTE[0].ROUTEEN = GPIO_TIMER_ROUTEEN_CC0PEN | GPIO_TIMER_ROUTEEN_CC1PEN;
  GPIO->TIMERROUTE[0].CC0ROUTE = (PWM1_PORT << _GPIO_TIMER_CC0ROUTE_PORT_SHIFT) | (PWM1_PIN << _GPIO_TIMER_CC0ROUTE_PIN_SHIFT);
  GPIO->TIMERROUTE[0].CC1ROUTE = (PWM2_PORT << _GPIO_TIMER_CC1ROUTE_PORT_SHIFT) | (PWM2_PIN << _GPIO_TIMER_CC1ROUTE_PIN_SHIFT);
  TIMER_InitCC(TIMER0, 0, &ccInit);
  TIMER_InitCC(TIMER0, 1, &ccInit);
  uint32_t top = CMU_ClockFreqGet(cmuClock_TIMER0) / PWM_FREQ;
  TIMER_TopSet(TIMER0, top);
  TIMER_CompareSet(TIMER0, 0, (top * dutyCycle1) / 100);
  TIMER_CompareSet(TIMER0, 1, (top * dutyCycle2) / 100);
  TIMER_Enable(TIMER0, true);
}
void motor1_forward(void) { GPIO_PinOutSet(LPWM1_PORT, LPWM1_PIN); GPIO_PinOutClear(RPWM1_PORT, RPWM1_PIN); }
void motor1_backward(void) { GPIO_PinOutClear(LPWM1_PORT, LPWM1_PIN); GPIO_PinOutSet(RPWM1_PORT, RPWM1_PIN); }
void motor2_forward(void) { GPIO_PinOutSet(LPWM2_PORT, LPWM2_PIN); GPIO_PinOutClear(RPWM2_PORT, RPWM2_PIN); }
void motor2_backward(void) { GPIO_PinOutClear(LPWM2_PORT, LPWM2_PIN); GPIO_PinOutSet(RPWM2_PORT, RPWM2_PIN); }
