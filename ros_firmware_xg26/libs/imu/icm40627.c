#include <libs/imu/icm40627.h>


float accel_bias[3] = {0};
float gyro_bias[3]  = {0};

void imu_init(void)
{
    GPIO_PinOutSet(gpioPortA, 10);
    sl_icm40627_spi_init();
    sl_icm40627_init();
    sl_icm40627_calibrate_accel_and_gyro(accel_bias, gyro_bias);
    sl_icm40627_enable_sensor(true, true, true);
}


static void float_to_str(char *buf, float val, int decimals) {
    int sign = (val < 0) ? -1 : 1;
    float abs_val = fabsf(val);

    float rounded = abs_val + 0.5f / powf(10, decimals);

    int32_t int_part = (int32_t)rounded;
    int32_t frac_part = (int32_t)((rounded - int_part) * powf(10, decimals));

    sprintf(buf, "%s%ld.%0*ld",
            (sign < 0) ? "-" : "",
            int_part, decimals, frac_part);
}

IMU_Data imu_read(void) {
    IMU_Data data;

    float accel[3], gyro[3];

    sl_icm40627_accel_read_data(accel);
    sl_icm40627_gyro_read_data(gyro);

    for (int i = 0; i < 3; i++) {
        data.accel[i] = accel[i] - accel_bias[i];
        data.gyro[i]  = gyro[i]  - gyro_bias[i];
     }

    char accel_str[3][16], gyro_str[3][16];
    for (int i = 0; i < 3; i++)
    {
       float_to_str(accel_str[i], accel[i], 3);
       float_to_str(gyro_str[i], gyro[i], 3);
     }
//    char buffer[128];
//    snprintf(buffer, sizeof(buffer),
//                 "Linear Accel[g]: X=%s, Y=%s, Z=%s\r\nGyro[°/s]: X=%s, Y=%s, Z=%s\r\n",
//                 accel_str[0], accel_str[1], accel_str[2],
//                 gyro_str[0], gyro_str[1], gyro_str[2]);
//
//   uart_send(buffer, strlen(buffer));

   return data;

}
