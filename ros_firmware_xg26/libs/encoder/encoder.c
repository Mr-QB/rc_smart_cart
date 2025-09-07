#include "encoder.h"
#include "sl_sleeptimer.h"

volatile int lastEncoded1 = 0;
volatile int lastEncoded2 = 0;
volatile int32_t lastEncoderCount1 = 0;
volatile int32_t lastEncoderCount2 = 0;
volatile int32_t encoderCount1 = 0;
volatile int32_t encoderCount2 = 0;
static float speed1_mps = 0.0f;
static float speed2_mps = 0.0f;

static void encoder1_ISR(void)
{
  int MSB = GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN);
  int LSB = GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded1 << 2) | encoded;
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderCount1--;
  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderCount1++;
  lastEncoded1 = encoded;
}

static void encoder2_ISR(void)
{
  int MSB = GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN);
  int LSB = GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded2 << 2) | encoded;
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderCount2--;
  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderCount2++;
  lastEncoded2 = encoded;
}

void encoder_gpio_callback(uint8_t pin)
{ // lỗi ở đây, check lại giúp anh nhé......
  switch (pin) {
    case ENC1A_PIN: case ENC1B_PIN: encoder1_ISR(); break;
    case ENC2A_PIN: case ENC2B_PIN: encoder2_ISR(); break;
    default: break;
  }
}

void encoder_update_speed(void)
{
    static uint64_t last_tick = 0;
    uint64_t now_tick = sl_sleeptimer_get_tick_count64();

    float deltaTime;
    if (last_tick == 0) {
        last_tick = now_tick;
        return;
    } else {
        uint64_t delta_tick = now_tick - last_tick;
        deltaTime = sl_sleeptimer_tick_to_ms(delta_tick) / 1000.0f;
    }

    if (deltaTime < (UPDATE_INTERVAL_MS/1000.0f) ){
        return;
    }
    last_tick = now_tick;

    int32_t currentCount1 = encoder1_get_count();
    int32_t currentCount2 = encoder2_get_count();

    int32_t deltaCount1 = currentCount1 - lastEncoderCount1;
    int32_t deltaCount2 = currentCount2 - lastEncoderCount2;

    float rev1 = (float)deltaCount1 / ENCODER_PPR;
    float rev2 = (float)deltaCount2 / ENCODER_PPR;

    float distance1 = 2 * 3.1415926f * WHEEL_RADIUS_M * rev1;
    float distance2 = 2 * 3.1415926f * WHEEL_RADIUS_M * rev2;

    speed1_mps = distance1 / deltaTime;
    speed2_mps = distance2 / deltaTime;

    lastEncoderCount1 = currentCount1;
    lastEncoderCount2 = currentCount2;
}

void encoder_init(void)
{
  CMU_ClockEnable(cmuClock_GPIO, true);
  GPIOINT_Init();
  GPIO_PinModeSet(ENC1A_PORT, ENC1A_PIN, gpioModeInputPull, 1);
  GPIO_PinModeSet(ENC1B_PORT, ENC1B_PIN, gpioModeInputPull, 1);
  GPIO_PinModeSet(ENC2A_PORT, ENC2A_PIN, gpioModeInputPull, 1);
  GPIO_PinModeSet(ENC2B_PORT, ENC2B_PIN, gpioModeInputPull, 1);
  lastEncoded1 = (GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN) << 1) | GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
  lastEncoded2 = (GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN) << 1) | GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
  GPIO_IntClear(0xFFFFFFFF);
  GPIO_ExtIntConfig(ENC1A_PORT, ENC1A_PIN, ENC1A_PIN, true, true, true);
  GPIO_ExtIntConfig(ENC1B_PORT, ENC1B_PIN, ENC1B_PIN, true, true, true);
  GPIO_ExtIntConfig(ENC2A_PORT, ENC2A_PIN, ENC2A_PIN, true, true, true);
  GPIO_ExtIntConfig(ENC2B_PORT, ENC2B_PIN, ENC2B_PIN, true, true, true);
  GPIOINT_CallbackRegister(ENC1A_PIN, encoder_gpio_callback);
  GPIOINT_CallbackRegister(ENC1B_PIN, encoder_gpio_callback);
  GPIOINT_CallbackRegister(ENC2A_PIN, encoder_gpio_callback);
  GPIOINT_CallbackRegister(ENC2B_PIN, encoder_gpio_callback);
  GPIO_IntEnable(1 << ENC1A_PIN); GPIO_IntEnable(1 << ENC1B_PIN); GPIO_IntEnable(1 << ENC2A_PIN); GPIO_IntEnable(1 << ENC2B_PIN);
  NVIC_ClearPendingIRQ(GPIO_ODD_IRQn); NVIC_EnableIRQ(GPIO_ODD_IRQn);
  NVIC_ClearPendingIRQ(GPIO_EVEN_IRQn); NVIC_EnableIRQ(GPIO_EVEN_IRQn);
}


int32_t encoder1_get_count(void)
{
  return encoderCount2;
}
int32_t encoder2_get_count(void)
{
  return encoderCount1;
}
float encoder1_get_speed_mps(void)
{
    return speed2_mps;
}

float encoder2_get_speed_mps(void)
{
    return speed1_mps;
}
