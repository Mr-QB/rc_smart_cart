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



#include <stdio.h>
#include <string.h>

#include "sl_iostream.h"
#include "sl_iostream_handles.h"
#include "app_iostream_usart.h"
#include "encoder.h"
#include "sl_sleeptimer.h"

#define BUFSIZE 64
#define SEND_INTERVAL_MS 100  // Gửi dữ liệu mỗi 10ms

static char buffer[BUFSIZE];
static uint64_t last_send_tick = 0;

void app_iostream_usart_init(void)
{
  encoder_init();  // Khởi tạo encoder

#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
#endif

  sl_iostream_set_default(sl_iostream_vcom_handle);  // Dùng VCOM làm stream mặc định
  sl_sleeptimer_init();  // Khởi tạo sleeptimer
  last_send_tick = sl_sleeptimer_get_tick_count64();

}

int32_t app_iostream_usart_process_action(void)
{
  uint64_t now_tick;
  now_tick = sl_sleeptimer_get_tick_count64();


  last_send_tick = now_tick;

      int32_t count1 = encoder1_get_count();


      int32_t count2 = encoder2_get_count();

      snprintf(buffer, sizeof(buffer), "ENC1: %ld | ENC2: %ld\r\n", count1, count2);
      sl_iostream_write(SL_IOSTREAM_STDOUT, buffer, strlen(buffer));
      return count1;

}



