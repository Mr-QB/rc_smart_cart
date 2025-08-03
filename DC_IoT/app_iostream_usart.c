//#include <stdio.h>
//#include <string.h>
//#include "sl_iostream.h"
//#include "app_iostream_usart.h"
//#include "sl_iostream_handles.h"
//#include "encoder.h"
//
//
//#define BUFSIZE 32
//static char buffer[BUFSIZE];
//
//
//void app_iostream_usart_init(void)
//{
//  encoder_init();
//#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
//  setvbuf(stdout, NULL, _IONBF, 0);
//  setvbuf(stdin, NULL, _IONBF, 0);
//#endif
//
//  sl_iostream_set_default(sl_iostream_vcom_handle);  // Chọn VCOM làm luồng mặc định
//
//}
//
//void app_iostream_usart_process_action(void)
//{
//
//     int32_t count1 = encoder1_get_count();
//     int32_t count2 = encoder2_get_count();
//
//     snprintf(buffer, sizeof(buffer), "ENC1: %ld | ENC2: %ld\r\n", count1, count2);
//     sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
//
//}



//#include <stdio.h>
//#include <string.h>
//
//#include "sl_iostream.h"
//#include "sl_iostream_handles.h"
//#include "app_iostream_usart.h"
//#include "encoder.h"
//#include "sl_sleeptimer.h"
//
//#define BUFSIZE 64
//#define SEND_INTERVAL_MS 100  // Gửi dữ liệu mỗi 10ms
//
//static char buffer[BUFSIZE];
//static uint64_t last_send_tick = 0;
//
//void app_iostream_usart_init(void)
//{
//  encoder_init();  // Khởi tạo encoder
//
//#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
//  setvbuf(stdout, NULL, _IONBF, 0);
//  setvbuf(stdin, NULL, _IONBF, 0);
//#endif
//
//  sl_iostream_set_default(sl_iostream_vcom_handle);  // Dùng VCOM làm stream mặc định
//  sl_sleeptimer_init();  // Khởi tạo sleeptimer
//  last_send_tick = sl_sleeptimer_get_tick_count64();
//
//}
//
//int32_t app_iostream_usart_process_action(void)
//{
//  uint64_t now_tick;
//  now_tick = sl_sleeptimer_get_tick_count64();
//
//
//  last_send_tick = now_tick;
//
//      int32_t count1 = encoder1_get_count();
//      int32_t count2 = encoder2_get_count();
//
//      snprintf(buffer, sizeof(buffer), "ENC1: %ld | ENC2: %ld\r\n", count1, count2);
//      sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
//      return count1;
//
//}
//
//#include <stdio.h>
//#include <string.h>
//#include "sl_iostream.h"
//#include "sl_iostream_handles.h"
//#include "app_iostream_usart.h"
//#include "encoder.h"
//#include "sl_sleeptimer.h"
//#include "motor_pwm.h"
//#include "kinematics.h"
//
//
//
//
//#define BUFSIZE 128
//#define SEND_INTERVAL_MS 100
//
//static char buffer[BUFSIZE];
//static uint64_t last_send_tick = 0;
//
//void app_iostream_usart_init(void)
//{
//  encoder_init();
//  sl_sleeptimer_init();
//
//#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
//  setvbuf(stdout, NULL, _IONBF, 0);
//  setvbuf(stdin, NULL, _IONBF, 0);
//#endif
//
//  sl_iostream_set_default(sl_iostream_vcom_handle);
//  last_send_tick = sl_sleeptimer_get_tick_count64();
//}
//
//void app_iostream_usart_process_action(void)
//{
//  uint64_t now_tick = sl_sleeptimer_get_tick_count64();
//  uint64_t elapsed_ms = sl_sleeptimer_tick_to_ms(now_tick - last_send_tick);
//
//  if (elapsed_ms >= SEND_INTERVAL_MS)
//  {
//    last_send_tick = now_tick;
//
//    int32_t count1 = encoder1_get_count();
//    int32_t count2 = encoder2_get_count();
//
//    // Truy cập vị trí robot từ kinematics.c
//    float x = robotPosition.x;
//    float y = robotPosition.y;
//    float theta = robotPosition.degree;
//
//    // PWM duty cycle của 2 động cơ
//    float pwm1 = dutyCycle1;
//    float pwm2 = dutyCycle2;
//
//    snprintf(buffer, sizeof(buffer),
//             "ENC1: %ld\t ENC2: %ld\t PWM1: %.2f\t PWM2: %.2f\t X: %.2f\t Y: %.2f\t Th: %.2f\r\n",
//             count1,
//             count2,
//             pwm1,
//             pwm2,
//             x,
//             y,
//             theta);
//
//    sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
//  }
//}


//#include <stdio.h>
//#include <string.h>
//#include "sl_iostream.h"
//#include "sl_iostream_handles.h"
//#include "app_iostream_usart.h"
//#include "encoder.h"
//#include "sl_sleeptimer.h"
//#include "motor_pwm.h"
//#include "kinematics.h"
//
//#define BUFSIZE 128
//#define SEND_INTERVAL_MS 100
//
//static char buffer[BUFSIZE];
//static uint64_t last_send_tick = 0;
//
//void app_iostream_usart_init(void)
//{
//  encoder_init();
//  sl_sleeptimer_init();
//
//#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
//  setvbuf(stdout, NULL, _IONBF, 0);
//  setvbuf(stdin, NULL, _IONBF, 0);
//#endif
//
//  sl_iostream_set_default(sl_iostream_vcom_handle);
//  last_send_tick = sl_sleeptimer_get_tick_count64();
//}
//
//void app_iostream_usart_process_action(void)
//{
//  uint64_t now_tick = sl_sleeptimer_get_tick_count64();
//  uint64_t elapsed_ms = sl_sleeptimer_tick_to_ms(now_tick - last_send_tick);
//
//  if (elapsed_ms >= SEND_INTERVAL_MS)
//  {
//    last_send_tick = now_tick;
//
//    int32_t count1 = encoder1_get_count();
//    int32_t count2 = encoder2_get_count();
//
//    float x = robotPosition.x;
//    float y = robotPosition.y;
//    float theta = robotPosition.theta;
//
//    float pwm1 = dutyCycle1;
//    float pwm2 = dutyCycle2;
//
//    // Gửi dữ liệu cho ROS
//    snprintf(buffer, sizeof(buffer),
//             "O %.3f %.3f %.3f 0.0 0.0 0.0\r\n",
//             x, y, theta);
//    sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
//
//    // Gửi debug
//    snprintf(buffer, sizeof(buffer),
//             "ENC1: %ld\t ENC2: %ld\t PWM1: %.2f\t PWM2: %.2f\t X: %.2f\t Y: %.2f\t Th: %.2f\r \n\n",
//             count1,
//             count2,
//             pwm1,
//             pwm2,
//             x,
//             y,
//             robotPosition.degree);
//
//    sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
//  }
//}
//


#include "app_iostream_usart.h"
#include "encoder.h"
#include "kinematics.h"
#include "motor_pwm.h"
#include "uart_odom_msg.h"
#include <stdio.h>
#include <string.h>
#include "sl_iostream.h"
#include "sl_iostream_handles.h"
#include "sl_sleeptimer.h"

#define BUFSIZE 128
#define SEND_INTERVAL_MS 1

static Odom_Msg_Bfr odom_bfr;
static uint64_t last_send_tick = 0;
static uint8_t paused = 0;

void app_iostream_usart_init(void) {
  encoder_init();
  sl_sleeptimer_init();
#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
#endif
  sl_iostream_set_default(sl_iostream_vcom_handle);
  last_send_tick = sl_sleeptimer_get_tick_count64();
}

void process_uart_command(void) {
  uint8_t cmd;
  size_t read_len;
  while (sl_iostream_read(SL_IOSTREAM_STDOUT, &cmd, 1, &read_len) == SL_STATUS_OK && read_len == 1) {
    switch (cmd) {
      case 'W': motor1_forward(); motor2_forward(); paused = 0; break;
      case 'S': motor1_backward(); motor2_backward(); paused = 0; break;
      case 'A': motor1_backward(); motor2_forward(); paused = 0; break;
      case 'D': motor1_forward(); motor2_backward(); paused = 0; break;
      case 'X': dutyCycle1 = 0; dutyCycle2 = 0; paused = 1; break;
      case 'P': paused = 1; dutyCycle1 = 0; dutyCycle2 = 0; break;
      case 'R': encoder_init(); break;
      case 'B': paused = 0; break;
      default: break;
    }
  }
}

void app_iostream_usart_process_action(void) {
  process_uart_command();

  uint64_t now_tick = sl_sleeptimer_get_tick_count64();
  uint64_t elapsed_ms = sl_sleeptimer_tick_to_ms(now_tick - last_send_tick);
  if (elapsed_ms >= SEND_INTERVAL_MS) {
    last_send_tick = now_tick;

        //bổ sung in test
        int32_t count1 = encoder1_get_count();
        int32_t count2 = encoder2_get_count();
        float x = robotPosition.x;
        float y = robotPosition.y;
        float theta = robotPosition.theta;

        char buffer[128];
        snprintf(buffer, sizeof(buffer),
          "ENC1: %ld | ENC2: %ld | X: %.2f | Y: %.2f | Th: %.2f\r\n", count1, count2, x, y, theta);
        sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer)); // <-- Gửi ra UART (Serial)

    if (!paused) {
      odom_bfr.odom_msg.headerA = 0x00;
      odom_bfr.odom_msg.headerB = 0xFF;
      odom_bfr.odom_msg.seq++;
      odom_bfr.odom_msg.t_micro = now_tick;
      odom_bfr.odom_msg.x = robotPosition.x;
      odom_bfr.odom_msg.y = robotPosition.y;
      odom_bfr.odom_msg.th = robotPosition.theta;
      odom_bfr.odom_msg.v_x = 0;
      odom_bfr.odom_msg.v_y = 0;
      odom_bfr.odom_msg.omega = 0;

      sl_iostream_write(SL_IOSTREAM_STDOUT, odom_bfr.msg, sizeof(odom_bfr.msg));
    }
  }

}


