//#ifndef ENCODER_H
//#define ENCODER_H
//
//#include "em_gpio.h"
//#include "em_core.h"
//
//
//#include <stdint.h>
//
//
//int32_t encoder_get_count(void);
//
//void encoder_init(void);
//int32_t encoder1_get_count(void);
//int32_t encoder2_get_count(void);
//
//#endif // ENCODER_H


#ifndef ENCODER_H
#define ENCODER_H
#include <stdint.h>
void encoder_init(void);
int32_t encoder1_get_count(void);
int32_t encoder2_get_count(void);
#endif
