#ifndef LIBS_ENCODER_ENCODER_H_
#define LIBS_ENCODER_ENCODER_H_

#include <stdint.h>
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

#define ENCODER_PPR       1920     // Pulses Per Revolution
#define WHEEL_RADIUS_M    0.05f   // Wheel radius (unit: meter)
#define UPDATE_INTERVAL_MS 100    // Speed update interval (ms)


void encoder_init(void);
int32_t encoder1_get_count(void);
float encoder1_get_speed_mps(void);
float encoder2_get_speed_mps(void);
int32_t encoder2_get_count(void);
void encoder_update_speed(void);

#endif /* LIBS_ENCODER_ENCODER_H_ */
