#include "motor_control.h"

volatile float dutyCycle1 = INITIAL_DUTY_CYCLE;
volatile float dutyCycle2 = INITIAL_DUTY_CYCLE;

static PID_Controller pid1, pid2;
static uint32_t timerTop;

float targetSpeed1 = 0.0f; // m/s
float targetSpeed2 = 0.0f; // m/s

float deltaTime = UPDATE_INTERVAL_MS / 1000.0f;


void initCMU(void)
{
    CMU_ClockEnable(cmuClock_GPIO, true);
    CMU_ClockEnable(cmuClock_TIMER0, true);
}

void initGPIO(void)
{
  GPIO_PinModeSet(PWM1_PORT, PWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(LPWM1_PORT, LPWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(RPWM1_PORT, RPWM1_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(PWM2_PORT, PWM2_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(LPWM2_PORT, LPWM2_PIN, gpioModePushPull, 0);
  GPIO_PinModeSet(RPWM2_PORT, RPWM2_PIN, gpioModePushPull, 0);
}

void initTIMER(void)
{
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
  timerTop  = CMU_ClockFreqGet(cmuClock_TIMER0) / PWM_FREQ;
  TIMER_TopSet(TIMER0, timerTop);
  TIMER_CompareSet(TIMER0, 0, (timerTop * dutyCycle1) / 100);
  TIMER_CompareSet(TIMER0, 1, (timerTop * dutyCycle2) / 100);
  TIMER_Enable(TIMER0, true);
}

void motor1_set_direction(int8_t dir)
{
    if (dir >= 0) {
        GPIO_PinOutSet(LPWM1_PORT, LPWM1_PIN);
        GPIO_PinOutClear(RPWM1_PORT, RPWM1_PIN);
    } else {
        GPIO_PinOutClear(LPWM1_PORT, LPWM1_PIN);
        GPIO_PinOutSet(RPWM1_PORT, RPWM1_PIN);
    }
}

void motor2_set_direction(int8_t dir)
{
    if (dir >= 0) {
        GPIO_PinOutSet(LPWM2_PORT, LPWM2_PIN);
        GPIO_PinOutClear(RPWM2_PORT, RPWM2_PIN);
    } else {
        GPIO_PinOutClear(LPWM2_PORT, LPWM2_PIN);
        GPIO_PinOutSet(RPWM2_PORT, RPWM2_PIN);
    }
}

void motor_control_init(void) {
    initCMU();
    initGPIO();
    initTIMER();

    pid_init(&pid1, 100.0f, 10.0f, 10.05f,0.0f, 100.0f);
    pid_init(&pid2, 100.0f, 10.0f, 10.05f, 0.0f, 100.0f);
}

void motor_control_update(void) {
    float actualSpeed1 = encoder1_get_speed_mps();
    float actualSpeed2 = encoder2_get_speed_mps();

    float duty1 = pid_compute(&pid1, targetSpeed1, actualSpeed1, deltaTime);
    float duty2 = pid_compute(&pid2, targetSpeed2, actualSpeed2, deltaTime);

    motor1_set_direction(duty1);
    motor2_set_direction(duty2);

    if (duty1 < 0) duty1 = -duty1;
    if (duty2 < 0) duty2 = -duty2;

    if (duty1 > 100.0f) duty1 = 100.0f;
    if (duty2 > 100.0f) duty2 = 100.0f;

    TIMER_CompareSet(TIMER0, 0, (uint32_t)(timerTop * duty1 / 100.0f));
    TIMER_CompareSet(TIMER0, 1, (uint32_t)(timerTop * duty2 / 100.0f));
}

void motor1_set_target_speed(float speed_mps) {
    targetSpeed1 = speed_mps;
}

void motor2_set_target_speed(float speed_mps) {
    targetSpeed2 = speed_mps;
}

