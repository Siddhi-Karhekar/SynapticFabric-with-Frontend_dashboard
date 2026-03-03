def simulate(temp, torque, air):

    heat = 0.0005 * torque**2
    cooling = 0.1 * (temp - air)

    return temp + heat - cooling