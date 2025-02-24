import math
from time import sleep

from stepper import Stepper

track_width = 97       # width from center of front left wheel to center of front right wheel
full_turn_mm = track_width * math.pi
wheel_dia = 66
rot_mm = wheel_dia * math.pi


def get_steps_for_mm(mm, half=False):
    steps_per_rot = 2048
    if half:
        steps_per_rot = 4096
    return round(steps_per_rot/rot_mm*mm)


def get_steps_for_deg(deg, half=False):
    dist = full_turn_mm / 360.0 * deg
    return get_steps_for_mm(dist, half)


def drive(mm, forward=True):
    steps = get_steps_for_mm(mm)
    print(steps)
    for i in range(steps):
        #for t in range(0, 4):
        step_l.tick(forward)
        step_r.tick(forward)
        sleep(0.002)


def turn(deg, right=True):
    steps = get_steps_for_deg(deg)
    print(steps)
    for i in range(steps):
        step_l.tick(right)
        step_r.tick(not right)
        sleep(0.002)


def circle(dia, cw=True):
    outer = dia * math.pi
    outer_steps = get_steps_for_mm(outer)
    inner = (dia - track_width * 2) * math.pi
    inner_steps = get_steps_for_mm(inner)
    ratio = inner_steps / outer_steps
    last_inner_step = 0
    print(outer_steps, inner_steps, ratio)
    for i in range(outer_steps):
        step_l.tick(True) if cw else step_r.tick(True)
        last_inner_step = last_inner_step + ratio
        if last_inner_step > 1:
            step_r.tick(True) if cw else step_l.tick(True)
            last_inner_step = last_inner_step - 1
        sleep(0.002)


step_l = Stepper()
step_r = Stepper(False, [6, 7, 8, 9])

sleep(3)
try:
    #drive(3000, True)
    #turn(180)
    #drive(1000, True)
    circle(800.0)
except KeyboardInterrupt:
    f = False


