#include "uart.h"

#define BUFSIZE 128
#define SEND_INTERVAL_MS 1

static uint64_t last_send_tick = 0;


void app_iostream_usart_init(void) {
  sl_sleeptimer_init();
#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
#endif
  sl_iostream_set_default(sl_iostream_vcom_handle);
  last_send_tick = sl_sleeptimer_get_tick_count64();
}

void app_iostream_usart_process_action(const char *message) {
  uint64_t now_tick = sl_sleeptimer_get_tick_count64();
  uint64_t elapsed_ms = sl_sleeptimer_tick_to_ms(now_tick - last_send_tick);
  if (elapsed_ms >= SEND_INTERVAL_MS) {
    last_send_tick = now_tick;

    sl_iostream_write(SL_IOSTREAM_STDOUT, message, strlen(message));
    sl_iostream_write(SL_IOSTREAM_STDOUT, "\r\n", 2);
  }
}

void uart_send(const char *data, uint16_t len) {
    uint64_t now_tick = sl_sleeptimer_get_tick_count64();
    uint64_t elapsed_ms = sl_sleeptimer_tick_to_ms(now_tick - last_send_tick);
    if (elapsed_ms >= SEND_INTERVAL_MS) {
        last_send_tick = now_tick;

        sl_iostream_write(SL_IOSTREAM_STDOUT, data, len);
        sl_iostream_write(SL_IOSTREAM_STDOUT, "\r\n", 2);
      }


}


