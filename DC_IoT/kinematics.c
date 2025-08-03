//#include "kinematics.h"
//
//position_t robotPosition = {0};
//speed_t robotSpeed = {0};
//speed_on_map_t worldSpeed = {0};
//
//void update_position(int leftCount, int rightCount)
//{
//    robotSpeed.deltaLeft  = leftCount  * MM_PER_COUNT;
//    robotSpeed.deltaRight = rightCount * MM_PER_COUNT;
//
//    robotSpeed.deltaTheta = (robotSpeed.deltaLeft - robotSpeed.deltaRight) / WHEEL_DISTANCE;
//    robotSpeed.deltaS     = (robotSpeed.deltaLeft + robotSpeed.deltaRight) / 2.0;
//
//    if (fabs(robotSpeed.deltaTheta) > 1e-6) {
//        robotSpeed.deltaS = 2.0 * (robotSpeed.deltaS / robotSpeed.deltaTheta) *
//                            sin(robotSpeed.deltaTheta / 2.0);
//    }
//
//    worldSpeed.deltaX = robotSpeed.deltaS *
//                        cos(robotPosition.theta + robotSpeed.deltaTheta / 2.0);
//    worldSpeed.deltaY = robotSpeed.deltaS *
//                        sin(robotPosition.theta + robotSpeed.deltaTheta / 2.0);
//
//    robotPosition.x += worldSpeed.deltaX;
//    robotPosition.y += worldSpeed.deltaY;
//    robotPosition.theta += robotSpeed.deltaTheta;
//
//    // Giới hạn góc theta trong [0, 2*pi)
//    robotPosition.theta = fmod(robotPosition.theta, 2.0 * M_PI);
//    if (robotPosition.theta < 0) {
//        robotPosition.theta += 2.0 * M_PI;
//    }
//
//    robotPosition.degree = robotPosition.theta * 180.0 / M_PI;
//}
//
//void update_speed(uint64_t deltaTime_ms)
//{
//    if (deltaTime_ms == 0) return;
//
//    robotSpeed.linear  = robotSpeed.deltaS * 1000.0 / deltaTime_ms;      // mm/ms
//    robotSpeed.angular = robotSpeed.deltaTheta * 1000.0 / deltaTime_ms; // rad/ms
//    robotSpeed.left    = robotSpeed.deltaLeft * 1000.0 / deltaTime_ms;
//    robotSpeed.right   = robotSpeed.deltaRight * 1000.0 / deltaTime_ms;
//
//    worldSpeed.x = worldSpeed.deltaX * 1000.0 / deltaTime_ms;
//    worldSpeed.y = worldSpeed.deltaY * 1000.0 / deltaTime_ms;
//}


//#include "kinematics.h"
//#include <math.h>
//
//
//#ifndef M_PI
//#define M_PI 3.14159265358979323846
//#endif
//#define TICKS_PER_REV 1920.0f
//#define WHEEL_DIAMETER 0.065f
//#define WHEEL_BASE 0.20f
//
//KinematicState robotPosition = {0};
//
//void update_position(int32_t delta_enc1, int32_t delta_enc2)
//{
//  float left_dist = (delta_enc1 / TICKS_PER_REV) * (M_PI * WHEEL_DIAMETER);
//  float right_dist = (delta_enc2 / TICKS_PER_REV) * (M_PI * WHEEL_DIAMETER);
//  float center_dist = (left_dist + right_dist) / 2.0f;
//  float delta_theta = (right_dist - left_dist) / WHEEL_BASE;
//
//  robotPosition.theta += delta_theta;
//  robotPosition.theta = fmod(robotPosition.theta, 2.0f * M_PI);
//
//  robotPosition.x += center_dist * cosf(robotPosition.theta);
//  robotPosition.y += center_dist * sinf(robotPosition.theta);
//  robotPosition.degree = robotPosition.theta * 180.0f / M_PI;
//}
//
//void update_speed(uint64_t delta_time_ms)
//{
//  (void)delta_time_ms;
//}


#include "kinematics.h"
#include "encoder.h"
#include <math.h>


#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#define TICKS_PER_REV 1920.0f
#define WHEEL_DIAMETER 97.2f
#define WHEEL_BASE 400.0f


KinematicState robotPosition = {0};
void update_position(int32_t delta_enc1, int32_t delta_enc2) {
  float left_dist = (delta_enc1 / TICKS_PER_REV) * (M_PI * WHEEL_DIAMETER);
  float right_dist = (delta_enc2 / TICKS_PER_REV) * (M_PI * WHEEL_DIAMETER);
  float center_dist = (left_dist + right_dist) / 2.0f;
  float delta_theta = (right_dist - left_dist) / WHEEL_BASE;
  robotPosition.theta += delta_theta;
  robotPosition.theta = fmodf(robotPosition.theta, 2.0f * M_PI);
  robotPosition.x += center_dist * cosf(robotPosition.theta);
  robotPosition.y += center_dist * sinf(robotPosition.theta);
  robotPosition.degree = robotPosition.theta * 180.0f / M_PI;
}
void update_speed(uint64_t delta_time_ms) { (void)delta_time_ms; }

