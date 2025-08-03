//#include "encoder.h"
//#include "motor_pwm.h"
//#include "sl_udelay.h"
//
//#include "app_iostream_usart.h"
//#include "sl_iostream.h"
//#include <string.h>
//
//#include <stdio.h>       // <- cần thêm để dùng snprintf
//
//void app_init(void)
//{
//  encoder_init();
//
//  app_iostream_usart_init();
//
//}
//
////void app_process_action(void)
////{
////      app_iostream_usart_process_action();
////
////}
//
//
//
//void app_loop(int time) {
//
//  dutyCycle1 = time;
//  dutyCycle2 = time;
//
//  motor1_forward();
//
//  motor2_backward();
//
//  uint32_t top = TIMER_TopGet(TIMER0);
//  TIMER_CompareSet(TIMER0, 0, (top * dutyCycle1) / 100);
//  TIMER_CompareSet(TIMER0, 1, (top * dutyCycle2) / 100);
//
//  //sl_udelay_wait(500000); // 0.5 giây delay
//}
//


//
//#include "encoder.h"
//#include "motor_pwm.h"
//#include "pid_position.h"
//#include "sl_udelay.h"
//#include "sl_iostream.h"
//#include "app_iostream_usart.h"
//#include <stdio.h>
//#include <string.h>
//#include <math.h>   // fabs()
//
//
//#define TARGET_PULSE       1920
//#define MIN_DUTY           0
//#define MAX_DUTY           100
//#define STOP_THRESHOLD     5  // Độ lệch cho phép
//
//void app_init(void)
//{
//  encoder_init();
//  initCMU();
//  initGPIO();
//  initTIMER();
//  app_iostream_usart_init();
//
//
//}
//
//void app_process_action(void)
//{
//
//  // Không dùng trong điều khiển vị trí liên tục
//}
//
//// Hàm chạy vòng lặp điều khiển
//void app_loop(void) {
//  int32_t target_position = 1920;//1920;
//  int32_t current_position = encoder1_get_count();
//
//  float duty = pid_position_compute(target_position, current_position);
//
//  // Giới hạn duty
//  if (duty > 100) duty = 100;
//  if (duty < 0) duty = 0;
//
//  // Nếu đã tới vị trí → dừng
//  if (abs(target_position - current_position) < 10) {
//    duty = 0;
//  }
//
//  dutyCycle1 = duty;
//  dutyCycle2 = duty;
//
//  // Điều khiển chiều quay
//  if (current_position < target_position) {
//    motor1_forward();
//    motor2_backward();
//  } else {
//    motor1_backward();
//    motor2_forward();
//  }
//
//  // Ghi giá trị PWM
//  uint32_t top = TIMER_TopGet(TIMER0);
//  TIMER_CompareSet(TIMER0, 0, (top * dutyCycle1) / 100);
//  TIMER_CompareSet(TIMER0, 1, (top * dutyCycle2) / 100);
//
//  // UART debug
//  //printf("Target: %ld | Pos: %ld | Duty: %.2f\r\n", target_position, current_position, duty);
//}
//

//
//#include "encoder.h"
//#include "motor_pwm.h"
//#include "kinematics.h"
//#include "sl_sleeptimer.h"
//
//static int32_t prev_enc1 = 0;
//static int32_t prev_enc2 = 0;
//static uint64_t last_tick = 0;
//
//void app_init(void)
//{
//  encoder_init();
//  last_tick = sl_sleeptimer_get_tick_count64();
//}
//
//void app_process_action(void)
//{
//  uint64_t now = sl_sleeptimer_get_tick_count64();
//  uint64_t delta_time = now - last_tick;
//  last_tick = now;
//
//  int32_t enc1 = encoder1_get_count();
//  int32_t enc2 = encoder2_get_count();
//
//  int32_t delta_enc1 = enc1 - prev_enc1;
//  int32_t delta_enc2 = enc2 - prev_enc2;
//
//  prev_enc1 = enc1;
//  prev_enc2 = enc2;
//
//  update_position(delta_enc1, delta_enc2);
//  update_speed(delta_time);
//}
//
//void app_loop(void) {
//
//  dutyCycle1 = 80;
//  dutyCycle2 = 80;
//
//  motor1_forward();
//  motor2_backward();
//
//  uint32_t top = TIMER_TopGet(TIMER0);
//  TIMER_CompareSet(TIMER0, 0, (top * dutyCycle1) / 100);
//  TIMER_CompareSet(TIMER0, 1, (top * dutyCycle2) / 100);
//
//
//}


#include "encoder.h"
#include "motor_pwm.h"
#include "kinematics.h"
#include "sl_sleeptimer.h"

static int32_t prev_enc1 = 0;
static int32_t prev_enc2 = 0;
static uint64_t last_tick = 0;

void app_init(void) {
  encoder_init();
  last_tick = sl_sleeptimer_get_tick_count64();
}

void app_process_action(void) {
  uint64_t now = sl_sleeptimer_get_tick_count64();
  uint64_t delta_time = now - last_tick;
  last_tick = now;

  int32_t enc1 = encoder1_get_count();
  int32_t enc2 = encoder2_get_count();

  int32_t delta_enc1 = enc1 - prev_enc1;
  int32_t delta_enc2 = enc2 - prev_enc2;

  prev_enc1 = enc1;
  prev_enc2 = enc2;

  update_position(delta_enc1, delta_enc2);
  update_speed(delta_time);
}

