
#include "odometry.h"
#include <math.h>
#include <stdio.h>
#include <string.h>

static odometry_t odom;

void odometry_init(void) {
    odom.x = 10.0f;
    odom.y = 10.0f;
    odom.theta = 0.0f; // rad
    odom.v = 0.0f;     // m/s
    odom.w = 0.0f;     // rad/s
    odom.v_left = 0.0f;
    odom.v_right = 0.0f;
}

void odometry_update(void) {
    float v_left  = encoder1_get_speed_mps();
    float v_right = encoder2_get_speed_mps();

    odom.v_left  = v_left;
    odom.v_right = v_right;

//    float v = (v_right + v_left) / 2.0f;
//    float w = (v_right - v_left) / WHEEL_BASE_M;
//    float dt = UPDATE_INTERVAL_MS / 1000.0f;
//
//    if (fabsf(w) < 1e-6f) {
//        odom.x += v * cosf(odom.theta) * dt;
//        odom.y += v * sinf(odom.theta) * dt;
//    } else {
//        float R = v / w;
//        float delta_theta = w * dt;
//        odom.x += R * (sinf(odom.theta + delta_theta) - sinf(odom.theta));
//        odom.y -= R * (cosf(odom.theta + delta_theta) - cosf(odom.theta));
//        odom.theta += delta_theta;
//    }
//
//    if (odom.theta > M_PI) odom.theta -= 2.0f * M_PI;
//    else if (odom.theta < -M_PI) odom.theta += 2.0f * M_PI;
//
//    odom.v = v;
//    odom.w = w;
}

void float_to_str(char *buf, float val, int decimals) {
    int sign = (val < 0) ? -1 : 1;
    float abs_val = fabsf(val);

    float rounded = abs_val + 0.5f / powf(10, decimals);

    int32_t int_part = (int32_t)rounded;
    int32_t frac_part = (int32_t)((rounded - int_part) * powf(10, decimals));

    sprintf(buf, "%s%ld.%0*ld",
            (sign < 0) ? "-" : "",
            int_part, decimals, frac_part);
}

void odometry_send_uart(void) {
    char buffer[128];
    char sx[16], sy[16], stheta[16], stheta_deg[16];
    char sv[16], sw[16], svl[16], svr[16];

    float theta_deg = odom.theta * 180.0f / M_PI;
    if (theta_deg > 180.0f)       theta_deg -= 360.0f;
    else if (theta_deg < -180.0f) theta_deg += 360.0f;

    float_to_str(sx,         odom.x,       3);
    float_to_str(sy,         odom.y,       3);
    float_to_str(stheta,     odom.theta,   3);
    float_to_str(stheta_deg, theta_deg,    3);
    float_to_str(sv,         odom.v,       3);
    float_to_str(sw,         odom.w,       3);
    float_to_str(svl,        odom.v_left,  3);
    float_to_str(svr,        odom.v_right, 3);

    // Gửi qua UART (thêm v_left & v_right)
    snprintf(buffer, sizeof(buffer),
             "ODOM %s %s %s %s %s %s %s %s",
             sx, sy, stheta, stheta_deg, sv, sw, svl, svr);

    uart_send(buffer, strlen(buffer));
}



