import time
import pygame

CAR_SPEED = 9
CAR_SPEED_CH = 2

class Brain:
    def __init__(self, database):
        self.database = database

    def run(self):
        time.sleep(0.5)
        while True:
            if self.database.stop:
                break

            time.sleep(0.001)
            _ = pygame.event.get()

            # Determine steering angle - using LiDAR data
            steer_angle = 0         # -8 ~ 8
            speed = CAR_SPEED       # 0 ~ 10
            lidar_data = self.database.lidar.data   # Array[180]

            rrr = lidar_data[20]
            rr = lidar_data[30]
            r = lidar_data[45]
            l = lidar_data[135]
            ll = lidar_data[150]
            lll = lidar_data[160]

            if lll < 60:
                steer_angle += 4
            if ll == 100:
                steer_angle -= 3
            if l == 100:
                steer_angle -= 2
            if r == 100:
                steer_angle += 2
            if rr == 100:
                steer_angle += 3
            if rrr < 60:
                steer_angle -= 4

            # Send controling data to the car
            if steer_angle > 0:
                self.right(steer_angle)
                if steer_angle >= 6:
                    speed -= 1
            else:
                self.left(-(steer_angle))
                if steer_angle <= -6:
                    speed -= 1
            
            # Velocity control
            if self.database.car.speed < speed:
                self.up(CAR_SPEED_CH)
            elif self.database.car.speed > speed:
                self.down(CAR_SPEED_CH)
            else:
                pass

    def up(self, num: int = 1):
        for i in range(num):
            self.database.control.up()

    def down(self, num: int = 1):
        for i in range(num):
            self.database.control.down()

    def right(self, num: int = 1):
        for i in range(num):
            self.database.control.right()

    def left(self, num: int = 1):
        for i in range(num):
            self.database.control.left()
