#ifndef ICM40627_H
#define ICM40627_H

#include "sl_status.h"
#include "sl_icm40627.h"
#include "sl_icm40627_config.h"
#include "../libs/uart/uart.h"
#include <stdio.h>
#include "em_gpio.h"
#include <stdio.h>
#include <stdint.h>
#include <math.h>

typedef struct {
    float accel[3]; // [g]
    float gyro[3];  // [°/s]
} IMU_Data;

void imu_init(void);
IMU_Data imu_read(void);

#endif // ICM40627_H
