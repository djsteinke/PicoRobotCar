from machine import Pin
from time import sleep

in1 = Pin(2, Pin.OUT)
in2 = Pin(3, Pin.OUT)
in3 = Pin(4, Pin.OUT)
in4 = Pin(5, Pin.OUT)

full_step = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
full_step_r = [[1, 0, 0, 1], [0, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0]]
half_step = [[0, 1, 1, 1], [0, 0, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1],
             [1, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0]]


class Stepper(object):
    def __init__(self, left=True, pins=None):
        global in1, in2, in3, in4
        if pins is not None:
            in1 = Pin(pins[0], Pin.OUT)
            in2 = Pin(pins[1], Pin.OUT)
            in3 = Pin(pins[2], Pin.OUT)
            in4 = Pin(pins[3], Pin.OUT)
        self.ins = [in1, in2, in3, in4]
        self.left = left
        self._i = 0

    def tick(self, forward=True):
        if not self.left:
            forward = not forward
        step_a = full_step if forward else full_step_r
        for t in range(4):
            self.ins[t].value(step_a[self._i][t])
        self._i = self._i + 1 if self._i < 3 else 0

    def step(self, forward=True):
        if not self.left:
            forward = not forward
        step_a = full_step if forward else full_step_r
        for s in step_a:
            for i in range(4):
                self.ins[i].value(s[i])
            sleep(0.002)

    def half_step(self, forward=True):
        if not self.left:
            forward = not forward
        for s in half_step:
            if forward:
                for i in range(8):
                    self.ins[i].value(s[i])
            else:
                for i in range(7, -1, -1):
                    self.ins[i].value(s[i])
            sleep(0.002)


