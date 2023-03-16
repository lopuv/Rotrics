import math
import numpy as np
import serial
import re


class Dexarm:

    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=None)
        self.is_open = self.ser.isOpen()
        if self.is_open:
            print('pydexarm: %s open' % self.ser.name)
        else:
            print('Failed to open serial port')

    def _send_cmd(self, data):
        self.ser.write(data.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("ok") > -1:
                    print("read ok")
                    break
                else:
                    print("read：", str)

    def go_home(self):
        self._send_cmd("M1112\r")

    def set_workorigin(self):
        self._send_cmd("G92 X0 Y0 Z0 E0\r")

    def set_acceleration(self, acceleration, travel_acceleration, retract_acceleration=60):
        cmd = "M204"+"P" + str(acceleration) + "T"+str(travel_acceleration) + "T" + str(retract_acceleration) + "\r\n"
        self._send_cmd(cmd)

    def set_module_kind(self, kind):
        self._send_cmd("M888 P" + str(kind) + "\r")

    def get_module_kind(self):
        self.ser.write('M888\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("PEN") > -1:
                    module_kind = 'PEN'
                if str.find("LASER") > -1:
                    module_kind = 'LASER'
                if str.find("PUMP") > -1:
                    module_kind = 'PUMP'
                if str.find("3D") > -1:
                    module_kind = '3D'
            if len(str) > 0:
                if str.find("ok") > -1:
                    return module_kind

    def move_to(self, x, y, z, feedrate=2000):
        cmd = "G1"+"F" + str(feedrate) + "X"+str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    def fast_move_to(self, x, y, z, feedrate=2000):
        cmd = "G0"+"F" + str(feedrate) + "X"+str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    def get_current_position(self):
        self.ser.write('M114\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    e = float(temp[3])
            if len(str) > 0:
                if str.find("DEXARM Theta") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    a = float(temp[0])
                    b = float(temp[1])
                    c = float(temp[2])
            if len(str) > 0:
                if str.find("ok") > -1:
                    return x,y,z,e,a,b,c

    """Delay"""
    def dealy_ms(self, value):
        self._send_cmd("G4 P" + str(value) + '\r')

    def dealy_s(self, value):
        self._send_cmd("G4 S" + str(value) + '\r')

    """SoftGripper & AirPicker"""
    def soft_gripper_pick(self):
        self._send_cmd("M1001\r")

    def soft_gripper_place(self):
        self._send_cmd("M1000\r")

    def soft_gripper_nature(self):
        self._send_cmd("M1002\r")

    def soft_gripper_stop(self):
        self._send_cmd("M1003\r")

    def air_picker_pick(self):
        self._send_cmd("M1000\r")

    def air_picker_place(self):
        self._send_cmd("M1001\r")

    def air_picker_nature(self):
        self._send_cmd("M1002\r")

    def air_picker_stop(self):
        self._send_cmd("M1003\r")

    """Laser"""
    def laser_on(self, value=0):
        self._send_cmd("M3 S" + str(value) + '\r')

    def laser_off(self):
        self._send_cmd("M5\r")

    """Conveyor Belt"""
    def conveyor_belt_forward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D0\r')
    def conveyor_belt_backward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D1\r')
    def conveyor_belt_stop(self, speed=0):
        self._send_cmd("M2013\r")

    """Rotate"""
    def rotate_clockwise(self, angle):
        self.set_module_kind(6)
        self._send_cmd("M2100\r")
        self._send_cmd("M2101 " + "R" + str(angle) + '\r')

    def rotate_counterwise(self, angle):
        self.set_module_kind(6)
        self._send_cmd("M2100\r")
        self._send_cmd("M2101 " + "R-" + str(angle) + "\r")

    def bereken_y(self, x, diameter):
        y = int(math.sqrt(diameter * diameter - x * x))
        return y

    def angle(self, x, y):
        return (90 - 180*math.atan2(y, x)) - 360

    def circle(self, diameter, segments):
        rangecompensatie = 250
        z_start = 0
        positions = np.linspace(0, 2 * np.pi, segments + 1)
        straal = diameter / 2
        self.move_to(straal, 0, 0)
        x = straal * np.cos(positions)
        y = straal * np.sin(positions)
        for i in range(segments):
            self.move_to(x[i + 1] + rangecompensatie, y[i + 1] + rangecompensatie, z_start)


        #
        # x = 0
        # oldcomp = 0
        # compensate = 0
        # while x <= diameter:
        #     y = int(self.bereken_y(x, diameter))
        #     # voeg waardes toe aan x en y arrays met offset om altijd positieve waardes te hebben
        #     # dexarm.moveto(x,y)
        #     oldcomp = compensate
        #     compensate = self.angle(x, y)
        #     self.dealy_ms(150)
        #     self.rotate_counterwise(int(compensate - oldcomp))
        #     self.dealy_ms(150)
        #     print(x + diameter + rangecompensatie, y + diameter + rangecompensatie, compensate, oldcomp, compensate - oldcomp)
        #     # de rotatie is 360 dit moet 180 zijn.
        #     self.move_to(int(x + diameter + rangecompensatie), int(y + diameter + rangecompensatie), z_start)
        #     x += 1  # de volgende positie op de x-as
        #
        # x = diameter
        # while x >= (0-diameter):
        #     y = 0-int(self.bereken_y(x, diameter))
        #     # voeg waardes toe aan x en y arrays met offset om altijd positieve waardes te hebben
        #     oldcomp = compensate
        #     compensate = self.angle(x, y)
        #     self.dealy_ms(150)
        #     self.rotate_clockwise(int(compensate - oldcomp))
        #     self.dealy_ms(150)
        #     print(x+diameter, y+diameter+rangecompensatie)
        #     self.move_to(x+diameter, y+diameter+rangecompensatie, z_start)
        #     x -= 1
