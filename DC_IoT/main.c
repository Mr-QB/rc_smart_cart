//#include "app_iostream_usart.h"
//#include "em_chip.h"
//#include "motor_pwm.h"
//#include "app.h"
//
//
//#include "sl_component_catalog.h"
//#include "sl_main_init.h"
//#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
//#include "sl_power_manager.h"
//#endif
//#if defined(SL_CATALOG_KERNEL_PRESENT)
//#include "sl_main_kernel.h"
//#else // SL_CATALOG_KERNEL_PRESENT
//#include "sl_main_process_action.h"
//#endif // SL_CATALOG_KERNEL_PRESENT
//
//
//int main(void) {
//
//  sl_main_init();
//
//   #if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
//
//    sl_main_kernel_start();
//  #else // SL_CATALOG_KERNEL_PRESENT
//
//    // User provided code.
//
//  //CHIP_Init();
//  initCMU();
//  initGPIO();
//  initTIMER();
//  //encoder_init();
//  int32_t encoder1 = app_iostream_usart_process_action();
//
//  app_iostream_usart_init();
//  app_loop(40);
//  while (1) {
//      sl_main_process_action();
//      encoder1 = app_iostream_usart_process_action();
//      if(encoder1>=1920*2){
//          app_loop(0);
//      }
//      else{
//          app_loop(80);
//      }
//   #if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
//    // Let the CPU go to sleep if the system allows it.
//    sl_power_manager_sleep();
//#endif
//
//  }
//#endif
//}

//#include "app_iostream_usart.h"
//#include "motor_pwm.h"
//#include "app.h"
//#include "sl_component_catalog.h"
//#include "sl_main_init.h"
//#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
//#include "sl_power_manager.h"
//#endif
//#if defined(SL_CATALOG_KERNEL_PRESENT)
//#include "sl_main_kernel.h"
//#else
//#include "sl_main_process_action.h"
//#endif
//
//int main(void)
//{
//  sl_main_init();
//
//#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
//  sl_main_kernel_start();
//#else
//  initCMU();
//  initGPIO();
//  initTIMER();
//  app_iostream_usart_init();
//  app_init();
//
//  while (1)
//  {
//    sl_main_process_action();
//    app_process_action();
//    app_iostream_usart_process_action();
//  }
//#endif
//}


#include "app.h"
#include "motor_pwm.h"
#include "encoder.h"
#include "kinematics.h"
#include "sl_main_init.h"
#include "app_iostream_usart.h"
#include "sl_main_process_action.h"

int main(void) {
  sl_main_init();
  SystemInit();
   initCMU();
   initGPIO();
   initTIMER();
   app_init();
   app_iostream_usart_init();

  while (1) {
    sl_main_process_action();
    app_process_action();            // Cập nhật encoder, tính toán vị trí
    app_iostream_usart_process_action(); // Gửi dữ liệu odometry cho ROS (nhị phân + nhận lệnh UART)
  }
}
