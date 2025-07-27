#ifndef APP_IOSTREAM_USART_H_
#define APP_IOSTREAM_USART_H_

#include <stdint.h>
#include <stdbool.h>

// Hàm khởi tạo USART
void app_iostream_usart_init(void);
int32_t app_iostream_usart_process_action(void);


// Hàm đọc dữ liệu encoder từ UART (nếu bạn cần tương tác 2 chiều)
bool app_iostream_usart_read_encoder(uint8_t *buffer, uint32_t buffer_size);

#endif /* APP_IOSTREAM_USART_H_ */
