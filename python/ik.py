import math
# 2 joint inverse kinematics functions

# Calculates the ik when q2 is positive, returns in radians
def calculatePositiveRad(x, y, a1, a2):
    q2 = math.acos((x**2 + y**2 - a1**2 - a2**2)/(2 * a1 * a2))
    q1 = math.atan2(x, y) - math.atan2((a1 + a2 * math.cos(q2)), (a2 * math.sin(q2)))
    #if x < 0:
    #    q1 -= math.pi
    return (q1, q2)

# Calculates ik when q2 is positive, returns in degrees
def calculatePositiveDeg(x, y, a1, a2):
    q1, q2 = calculatePositiveRad(x, y, a1, a2)
    return (math.degrees(q1), math.degrees(q2))

# Calculates ik when q2 is negative, returns in degrees
def calculateNegativeRad(x, y, a1, a2):
    q2 = -math.acos((x**2 + y**2 - a1**2 - a2**2)/(2 * a1 * a2))
    q1 = -(math.atan2(x, y) - math.atan2((a1 + a2 * math.cos(q2)), (a2 * math.sin(q2))))
    if x < 0:
        q1 -= 2 * math.pi
    return (q1, q2)

# Calculates ik when q2 is negative, returns in degrees
def calculateNegativeDeg(x, y, a1, a2):
    q1, q2 = calculateNegativeRad(x, y, a1, a2)
    return (math.degrees(q1), math.degrees(q2))