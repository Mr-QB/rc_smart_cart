#ifndef APP_IOSTREAM_USART_H_
#define APP_IOSTREAM_USART_H_

#include <stdio.h>
#include <string.h>
#include "sl_iostream.h"
#include "sl_iostream_handles.h"
#include "sl_sleeptimer.h"

void app_iostream_usart_init(void);
void app_iostream_usart_process_action(const char *message);
void uart_send(const char *data, uint16_t len);

#endif
