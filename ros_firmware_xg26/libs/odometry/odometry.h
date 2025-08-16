#ifndef LIBS_ODOMETRY_ODOMETRY_H_
#define LIBS_ODOMETRY_ODOMETRY_H_

#include <stdint.h>
#include "../libs/encoder/encoder.h"
#include "../libs/uart/uart.h"
#include <math.h>
#include <stdio.h>


#define WHEEL_BASE_M 0.365f          // Khoảng cách giữa 2 bánh (m)
#define M_PI  3.14159265358979323846

typedef struct {

    float x;      // [m]
    float y;      // [m]
    float theta;  // [rad]
    float v;      // [m/s]
    float w;      // [rad/s]
    float v_left;
    float v_right;
} odometry_t;

void odometry_init(void);
void odometry_update(void);
void odometry_send_uart(void);

#endif /* LIBS_ODOMETRY_ODOMETRY_H_ */
