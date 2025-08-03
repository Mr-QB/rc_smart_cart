//#ifndef KINEMATICS_H
//#define KINEMATICS_H
//
//#include <stdint.h>
//#include <math.h>
//
//#ifndef M_PI
//#define M_PI 3.14159265358979323846
//#endif
//
//#define RATIO             168.0         // Tỷ số truyền encoder
//#define PERIMETER         200.1         // Chu vi bánh xe (mm)
//#define MM_PER_COUNT      (PERIMETER / RATIO / 4.0)
//#define WHEEL_DISTANCE    400.5          // Khoảng cách 2 bánh xe (mm)
//
//// Cấu trúc lưu vị trí
//typedef struct {
//    double x;
//    double y;
//    double theta;   // radian
//    double degree;  // độ
//} position_t;
//
//// Cấu trúc tốc độ robot
//typedef struct {
//    double deltaLeft;
//    double deltaRight;
//    double deltaTheta;
//    double deltaS;
//    double linear;   // mm/ms
//    double angular;  // rad/ms
//    double left;
//    double right;
//} speed_t;
//
//// Tốc độ trong hệ tọa độ bản đồ
//typedef struct {
//    double deltaX;
//    double deltaY;
//    double x;
//    double y;
//} speed_on_map_t;
//
//// Biến toàn cục
//extern position_t robotPosition;
//extern speed_t robotSpeed;
//extern speed_on_map_t worldSpeed;
//
//// Hàm cập nhật
//void update_position(int leftCount, int rightCount);
//void update_speed(uint64_t deltaTime_ms);
//
//#endif


#ifndef KINEMATICS_H
#define KINEMATICS_H
#include <stdint.h>

typedef struct {
  float x;
  float y;
  float theta;
  float degree;
} KinematicState;

extern KinematicState robotPosition;

void update_position(int32_t delta_enc1, int32_t delta_enc2);
void update_speed(uint64_t delta_time_ms);

#endif
