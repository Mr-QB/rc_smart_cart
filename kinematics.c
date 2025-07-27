#include "kinematics.h"

position_t robotPosition = {0};
speed_t robotSpeed = {0};
speed_on_map_t worldSpeed = {0};

void update_position(int leftCount, int rightCount)
{
    robotSpeed.deltaLeft  = leftCount  * MM_PER_COUNT;
    robotSpeed.deltaRight = rightCount * MM_PER_COUNT;

    robotSpeed.deltaTheta = (robotSpeed.deltaLeft - robotSpeed.deltaRight) / WHEEL_DISTANCE;
    robotSpeed.deltaS     = (robotSpeed.deltaLeft + robotSpeed.deltaRight) / 2.0;

    if (fabs(robotSpeed.deltaTheta) > 1e-6) {
        robotSpeed.deltaS = 2.0 * (robotSpeed.deltaS / robotSpeed.deltaTheta) *
                            sin(robotSpeed.deltaTheta / 2.0);
    }

    worldSpeed.deltaX = robotSpeed.deltaS *
                        cos(robotPosition.theta + robotSpeed.deltaTheta / 2.0);
    worldSpeed.deltaY = robotSpeed.deltaS *
                        sin(robotPosition.theta + robotSpeed.deltaTheta / 2.0);

    robotPosition.x += worldSpeed.deltaX;
    robotPosition.y += worldSpeed.deltaY;
    robotPosition.theta += robotSpeed.deltaTheta;

    // Giới hạn góc theta trong [0, 2*pi)
    robotPosition.theta = fmod(robotPosition.theta, 2.0 * M_PI);
    if (robotPosition.theta < 0) {
        robotPosition.theta += 2.0 * M_PI;
    }

    robotPosition.degree = robotPosition.theta * 180.0 / M_PI;
}

void update_speed(uint64_t deltaTime_ms)
{
    if (deltaTime_ms == 0) return;

    robotSpeed.linear  = robotSpeed.deltaS * 1000.0 / deltaTime_ms;      // mm/ms
    robotSpeed.angular = robotSpeed.deltaTheta * 1000.0 / deltaTime_ms; // rad/ms
    robotSpeed.left    = robotSpeed.deltaLeft * 1000.0 / deltaTime_ms;
    robotSpeed.right   = robotSpeed.deltaRight * 1000.0 / deltaTime_ms;

    worldSpeed.x = worldSpeed.deltaX * 1000.0 / deltaTime_ms;
    worldSpeed.y = worldSpeed.deltaY * 1000.0 / deltaTime_ms;
}
