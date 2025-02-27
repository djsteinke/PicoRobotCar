import math
from time import sleep
import bluetooth
import time
from machine import Pin

from ble_simple_peripheral import BLESimplePeripheral
from stepper import Stepper

track_width = 107.5       # width from center of front left wheel to center of front right wheel
full_turn_mm = track_width * math.pi
wheel_dia = 66
rot_mm = wheel_dia * math.pi
delay = 0.0020
start_delay = 0.005
gear_ratio = 25.0/52.0/0.98


led = Pin("LED", Pin.OUT)
led_ticks = 0


def get_steps_for_mm(mm, half=False):
    steps_per_rot = 2048.0 * gear_ratio
    if half:
        steps_per_rot = 4096.0 * gear_ratio
    return round(steps_per_rot/rot_mm*mm)


def get_steps_for_deg(deg, half=False):
    dist = full_turn_mm / 360.0 * deg
    return get_steps_for_mm(dist, half)


def delay_clock():
    global delay
    if delay > 0.002:
        delay = round(delay - 0.0001, 4)
        print(delay)
    sleep(delay)


def drive(mm, forward=True):
    global delay
    delay = start_delay
    steps = get_steps_for_mm(mm)
    print(steps)
    for i in range(steps):
        #for t in range(0, 4):
        step_l.tick(forward)
        step_r.tick(forward)
        delay_clock()


def turn(deg, right=True):
    global delay
    delay = start_delay
    steps = get_steps_for_deg(deg)
    print(steps)
    for i in range(steps):
        step_l.tick(right)
        step_r.tick(not right)
        delay_clock()


def circle(dia, cw=True):
    global delay
    delay = start_delay
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
        delay_clock()


step_l = Stepper()
step_r = Stepper(False, [6, 7, 8, 9])


try:
    sleep(3)
    #drive(3000, True)
    #turn(180)
    #drive(1000, True)
    #circle(800.0)
except KeyboardInterrupt:
    f = False

ble = bluetooth.BLE()

sp = BLESimplePeripheral(ble)

led = Pin("LED", Pin.OUT)
led_state = 0

def on_rx(data):
    print("Data received: ", data)
    global led_state
    str_data = str(data, 'utf-8')
    if str_data.split("-")[0].startswith("toggle"):
        led.value(not led_state)
        led_state = 1 - led_state
    if str_data.split("-")[0].startswith("forward"):
        dist = int(str_data.split("-")[1])
        drive(dist)
        sp.send("complete")
    elif str_data.split("-")[0].startswith("backward"):
        dist = int(str_data.split("-")[1])
        drive(dist, False)
    elif str_data.split("-")[0].startswith("left"):
        dist = int(str_data.split("-")[1])
        turn(dist, False)
    elif str_data.split("-")[0].startswith("right"):
        dist = int(str_data.split("-")[1])
        turn(dist)


while True:
    if sp.is_connected():
        if led.value() == 0:
            led.on()
        sp.on_write(on_rx)
        #if complete:
        #    sp.send(b"1")
        #    complete = False
    else:
        if time.ticks_ms() - led_ticks > 500:
            led.toggle()
            led_ticks = time.ticks_ms()

