// //ngắt 4
//#include "encoder.h"
//#include "em_gpio.h"
//#include "em_cmu.h"
//#include "gpiointerrupt.h"
//#include <stdio.h>  // Thêm để debug
//
//// ----------------------
//// Define encoder pins
//// ----------------------
//
//// ENC1
//#define ENC1A_PORT gpioPortC
//#define ENC1A_PIN  10
//#define ENC1B_PORT gpioPortC
//#define ENC1B_PIN  11
//
//// ENC2
//#define ENC2A_PORT gpioPortC
//#define ENC2A_PIN  12
//#define ENC2B_PORT gpioPortC
//#define ENC2B_PIN  13
//
//// ----------------------
//// Encoder state & count
//// ----------------------
//
//volatile int lastEncoded1 = 0;
//volatile int lastEncoded2 = 0;
//volatile int32_t encoderCount1 = 0;
//volatile int32_t encoderCount2 = 0;
//
//// ----------------------
//// Quadrature decoder ISR
//// ----------------------
//
//static void encoder1_ISR(void)
//{
//  int MSB = GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN);
//  int LSB = GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
//  int encoded = (MSB << 1) | LSB;
//  int sum = (lastEncoded1 << 2) | encoded;
//
//  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
//    encoderCount1--;
//  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
//    encoderCount1++;
//
//  lastEncoded1 = encoded;
//}
//
//static void encoder2_ISR(void)
//{
//  int MSB = GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN);
//  int LSB = GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
//  int encoded = (MSB << 1) | LSB;
//  int sum = (lastEncoded2 << 2) | encoded;
//
//  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
//    encoderCount2--;
//  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
//    encoderCount2++;
//
//  lastEncoded2 = encoded;
//}
//
//// ----------------------
//// GPIO Callback handler
//// ----------------------
//
//void encoder_gpio_callback(uint8_t pin)
//{
//  switch (pin) {
//    case ENC1A_PIN:
//    case ENC1B_PIN:
//      encoder1_ISR();
//      break;
//    case ENC2A_PIN:
//    case ENC2B_PIN:
//      encoder2_ISR();
//      break;
//    default:
//      break;
//  }
//}
//
//// ----------------------
//// Encoder Initialization
//// ----------------------
//
//void encoder_init(void)
//{
//  CMU_ClockEnable(cmuClock_GPIO, true);
//  GPIOINT_Init();
//
//  // Configure pins
//  GPIO_PinModeSet(ENC1A_PORT, ENC1A_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC1B_PORT, ENC1B_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC2A_PORT, ENC2A_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC2B_PORT, ENC2B_PIN, gpioModeInputPull, 1);
//
//  // Read initial state
//  lastEncoded1 = (GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN) << 1) | GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
//  lastEncoded2 = (GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN) << 1) | GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
//
//  // Clear all previous interrupts
//  GPIO_IntClear(0xFFFFFFFF);
//
//  // Configure EXT interrupt and callback
//  GPIO_ExtIntConfig(ENC1A_PORT, ENC1A_PIN, ENC1A_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC1B_PORT, ENC1B_PIN, ENC1B_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC2A_PORT, ENC2A_PIN, ENC2A_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC2B_PORT, ENC2B_PIN, ENC2B_PIN, true, true, true);
//
//  GPIOINT_CallbackRegister(ENC1A_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC1B_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC2A_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC2B_PIN, encoder_gpio_callback);
//
//  // Enable interrupt mask for each pin
//  GPIO_IntEnable(1 << ENC1A_PIN);
//  GPIO_IntEnable(1 << ENC1B_PIN);
//  GPIO_IntEnable(1 << ENC2A_PIN);
//  GPIO_IntEnable(1 << ENC2B_PIN);
//
//  // Enable NVIC
//  NVIC_ClearPendingIRQ(GPIO_ODD_IRQn);
//  NVIC_EnableIRQ(GPIO_ODD_IRQn);
//  NVIC_ClearPendingIRQ(GPIO_EVEN_IRQn);
//  NVIC_EnableIRQ(GPIO_EVEN_IRQn);
//}
//
//// ----------------------
//// Encoder counter getters
//// ----------------------
//
//int32_t encoder1_get_count(void)
//{
//  return encoderCount1;
//}
//
//int32_t encoder2_get_count(void)
//{
//  return encoderCount2;
//}
//
//
//
//// ngắt 1
//
//

//
//#include "encoder.h"
//#include "em_gpio.h"
//#include "em_cmu.h"
//#include "gpiointerrupt.h"
//
//#define ENC1A_PORT gpioPortC
//#define ENC1A_PIN  10
//#define ENC1B_PORT gpioPortC
//#define ENC1B_PIN  11
//#define ENC2A_PORT gpioPortC
//#define ENC2A_PIN  12
//#define ENC2B_PORT gpioPortC
//#define ENC2B_PIN  13
//
//volatile int lastEncoded1 = 0;
//volatile int lastEncoded2 = 0;
//volatile int32_t encoderCount1 = 0;
//volatile int32_t encoderCount2 = 0;
//
//static void encoder1_ISR(void)
//{
//  int MSB = GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN);
//  int LSB = GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
//  int encoded = (MSB << 1) | LSB;
//  int sum = (lastEncoded1 << 2) | encoded;
//
//  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
//    encoderCount1--;
//  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
//    encoderCount1++;
//
//  lastEncoded1 = encoded;
//}
//
//static void encoder2_ISR(void)
//{
//  int MSB = GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN);
//  int LSB = GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
//  int encoded = (MSB << 1) | LSB;
//  int sum = (lastEncoded2 << 2) | encoded;
//
//  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
//    encoderCount2--;
//  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
//    encoderCount2++;
//
//  lastEncoded2 = encoded;
//}
//
//void encoder_gpio_callback(uint8_t pin)
//{
//  switch (pin) {
//    case ENC1A_PIN:
//    case ENC1B_PIN:
//      encoder1_ISR();
//      break;
//    case ENC2A_PIN:
//    case ENC2B_PIN:
//      encoder2_ISR();
//      break;
//    default:
//      break;
//  }
//}
//
//void encoder_init(void)
//{
//  CMU_ClockEnable(cmuClock_GPIO, true);
//  GPIOINT_Init();
//
//  GPIO_PinModeSet(ENC1A_PORT, ENC1A_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC1B_PORT, ENC1B_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC2A_PORT, ENC2A_PIN, gpioModeInputPull, 1);
//  GPIO_PinModeSet(ENC2B_PORT, ENC2B_PIN, gpioModeInputPull, 1);
//
//  lastEncoded1 = (GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN) << 1) | GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
//  lastEncoded2 = (GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN) << 1) | GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
//
//  GPIO_IntClear(0xFFFFFFFF);
//
//  GPIO_ExtIntConfig(ENC1A_PORT, ENC1A_PIN, ENC1A_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC1B_PORT, ENC1B_PIN, ENC1B_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC2A_PORT, ENC2A_PIN, ENC2A_PIN, true, true, true);
//  GPIO_ExtIntConfig(ENC2B_PORT, ENC2B_PIN, ENC2B_PIN, true, true, true);
//
//  GPIOINT_CallbackRegister(ENC1A_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC1B_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC2A_PIN, encoder_gpio_callback);
//  GPIOINT_CallbackRegister(ENC2B_PIN, encoder_gpio_callback);
//
//  GPIO_IntEnable(1 << ENC1A_PIN);
//  GPIO_IntEnable(1 << ENC1B_PIN);
//  GPIO_IntEnable(1 << ENC2A_PIN);
//  GPIO_IntEnable(1 << ENC2B_PIN);
//
//  NVIC_ClearPendingIRQ(GPIO_ODD_IRQn);
//  NVIC_EnableIRQ(GPIO_ODD_IRQn);
//  NVIC_ClearPendingIRQ(GPIO_EVEN_IRQn);
//  NVIC_EnableIRQ(GPIO_EVEN_IRQn);
//}
//
//int32_t encoder1_get_count(void) { return encoderCount1; }
//int32_t encoder2_get_count(void) { return encoderCount2; }


#include "encoder.h"
#include "em_gpio.h"
#include "em_cmu.h"
#include "gpiointerrupt.h"

#define ENC1A_PORT gpioPortC
#define ENC1A_PIN  10
#define ENC1B_PORT gpioPortC
#define ENC1B_PIN  11
#define ENC2A_PORT gpioPortC
#define ENC2A_PIN  12
#define ENC2B_PORT gpioPortC
#define ENC2B_PIN  13

volatile int lastEncoded1 = 0;
volatile int lastEncoded2 = 0;
volatile int32_t encoderCount1 = 0;
volatile int32_t encoderCount2 = 0;

static void encoder1_ISR(void) {
  int MSB = GPIO_PinInGet(ENC1A_PORT, ENC1A_PIN);
  int LSB = GPIO_PinInGet(ENC1B_PORT, ENC1B_PIN);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded1 << 2) | encoded;
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderCount1--;
  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderCount1++;
  lastEncoded1 = encoded;
}
static void encoder2_ISR(void) {
  int MSB = GPIO_PinInGet(ENC2A_PORT, ENC2A_PIN);
  int LSB = GPIO_PinInGet(ENC2B_PORT, ENC2B_PIN);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded2 << 2) | encoded;
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderCount2--;
  else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderCount2++;
  lastEncoded2 = encoded;
}
void encoder_gpio_callback(uint8_t pin) {
  switch (pin) {
    case ENC1A_PIN: case ENC1B_PIN: encoder1_ISR(); break;
    case ENC2A_PIN: case ENC2B_PIN: encoder2_ISR(); break;
    default: break;
  }
}
void encoder_init(void) {
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
int32_t encoder1_get_count(void) { return encoderCount1; }
int32_t encoder2_get_count(void) { return encoderCount2; }



