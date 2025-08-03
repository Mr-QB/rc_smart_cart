#ifndef ODOM_MSG_H_
#define ODOM_MSG_H_
#include <stdint.h>
#pragma pack(push, 1)
typedef struct {
    uint8_t headerA;      // 0x00
    uint8_t headerB;      // 0xFF
    uint16_t seq;
    uint32_t t_micro;
    float x, y, th;
    float v_x, v_y, omega;
} Odom_Msg;

typedef union {
    Odom_Msg odom_msg;
    uint8_t msg[32];
} Odom_Msg_Bfr;
#pragma pack(pop)
#endif
