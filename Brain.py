import time
import pygame
import math


CAR_SPEED = 9
CAR_SPEED_CH = 3

class Brain:
    def __init__(self, database):
        self.database = database

    def run(self):
        time.sleep(1)
        
        complete_list = []
        determine_complete_list = []
        parking_complete_list = []
        sign_mission_done = False
        car_stop = False
        parking_stop = False
        parking_out_done = False
        parking_direction_record = False
        while True:
            if self.database.stop:
                break

            time.sleep(0.001)
            _ = pygame.event.get()
            
            whole_v2x_data = self.database.v2x_data
            #print(whole_v2x_data)
            if len(whole_v2x_data) is 0:
                # 주행
                # ====================================================================================================================
                lidar_data = self.database.lidar.data

                rrr = lidar_data[20]
                rr = lidar_data[30]
                r = lidar_data[45]
                m = lidar_data[90]
                l = lidar_data[135]
                ll = lidar_data[150]
                lll = lidar_data[160]

                steer_angle = 0
                speed = CAR_SPEED

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

                if steer_angle > 0:
                    self.right(steer_angle)
                    if steer_angle >= 6:
                        speed -= 1
                else:
                    self.left(-(steer_angle))
                    if steer_angle <= -6:
                        speed -= 1
                #print(lll, ll, l, r, rr, rrr, steer_angle, speed)
                if car_stop is True:
                    speed = 0
                
                if self.database.car.speed < speed:
                    self.up(CAR_SPEED_CH)
                elif self.database.car.speed > speed:
                    self.down(CAR_SPEED_CH)
                else:
                    pass
                # ===================================================================================================================
            
            else:
                sign_key = 0
                # 표지판 있는지 검사
                for i in whole_v2x_data:
                    if whole_v2x_data[i][0] is "Left" or whole_v2x_data[i][0] is "Right":
                        sign_key = i
                # 표지판 미션의 key값 리턴

                # 있다면,
                if sign_key in whole_v2x_data:
                    if -60 < whole_v2x_data[i][1][0] - self.database.car.position[0] < 60:
                        # 표지판
                        # =================================================================================================================
                        if whole_v2x_data[i][0] is "Left":
                            # Left
                            left_wall_distance = self.database.lidar.data[160]
                            if left_wall_distance == 100:
                                self.left(4)
                        else:
                            # Right
                            right_wall_distance = self.database.lidar.data[20]
                            if right_wall_distance == 100:
                                self.right(4)

                        speed = 6
                        if self.database.car.speed < speed:
                            self.up()
                        elif self.database.car.speed > speed:
                            self.down()
                        else:
                            pass

                        # =================================================================================================================
                    
                    else:
                        # 신호등
                        # ===================================================================================================================
                        v2x_data = self.database.v2x_data
                        my_crosswalk = 0
                        for i in v2x_data:
                            if v2x_data[i][0] == 'Crosswalk':
                                if i in complete_list:
                                    continue
                                p_crosswalk = v2x_data[i][2]
                                p_curr = self.database.car.position

                                if -60 < p_crosswalk[0] - p_curr[0] < 60:
                                    if -50 < p_crosswalk[1] - p_curr[1] < 50: # 만약 신호등이 근처에 있다면
                                        my_crosswalk = i  # 우리가 보는 신호등이다.
                                        break

                        # 현재 신호등의 정보
                        if my_crosswalk in v2x_data:
                            curr_crosswalk = self.database.v2x_data[my_crosswalk]
                            # 현재 보고 있는 신호등 까지 구함.
                            
                            if my_crosswalk not in determine_complete_list:
                                if curr_crosswalk[1] == 'green':
                                    if curr_crosswalk[5] > 0.4*curr_crosswalk[6]:   # 충분한 시간이 남았을때, 통과
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = True
                                    determine_complete_list.append(my_crosswalk)

                                elif curr_crosswalk[1] == 'red':
                                    if curr_crosswalk[5] < 1:     # 빨간 불이 곧 끝남
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = True
                                    determine_complete_list.append(my_crosswalk)

                            else:
                                if curr_crosswalk[1] == 'green' :
                                    if curr_crosswalk[5] < 0.4*curr_crosswalk[6]:   # 계속 멈춰있어라.
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = False
                                        complete_list.append(my_crosswalk)
                                        time.sleep(0.001)

                                elif curr_crosswalk[1] == 'red':
                                    if curr_crosswalk[5] > 1:                       # 초록 신호로 바뀌기 직전
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = False
                                        complete_list.append(my_crosswalk)
                                        time.sleep(0.001)
                                
                            # 멈춰야하는지, 통과해야하는지 판단함.
                            #print(car_stop, complete_list, curr_crosswalk)
                        else:
                            pass

                        # ====================================================================================================================
                        
                        # 주행
                        # ====================================================================================================================
                        lidar_data = self.database.lidar.data

                        rrr = lidar_data[20]
                        rr = lidar_data[30]
                        r = lidar_data[45]
                        m = lidar_data[90]
                        l = lidar_data[135]
                        ll = lidar_data[150]
                        lll = lidar_data[160]

                        steer_angle = 0
                        speed = 7

                        if lll < 66:
                            steer_angle += 5
                        if ll == 100:
                            steer_angle -= 3
                        if l == 100:
                            steer_angle -= 2
                        if r == 100:
                            steer_angle += 2
                        if rr == 100:
                            steer_angle += 3
                        if rrr < 66:
                            steer_angle -= 5

                        if steer_angle > 0:
                            self.right(steer_angle)
                            if steer_angle >= 4:
                                speed -= 2
                        else:
                            self.left(-(steer_angle))
                            if steer_angle <= -4:
                                speed -= 2
                        if car_stop is True:
                            speed = 0
                        
                        if self.database.car.speed < speed:
                            self.up(2)
                        elif self.database.car.speed > speed:
                            self.down(2)
                        else:
                            pass
                        # ===================================================================================================================
                
                else:
                    # 주차 있는지 검사
                    parking_key = 0
                    for i in whole_v2x_data:
                        if whole_v2x_data[i][0] is "Parking":
                            parking_key = i
                    # 만약 주차 있다면
                    if parking_key in whole_v2x_data :
                        # 주차
                        # =================================================================================================================
                        v2x_data = self.database.v2x_data
                        my_parking = 0
                        for i in v2x_data:
                            if v2x_data[i][0] == "Parking":
                                if i in parking_complete_list:
                                    continue
                                p_parking = [v2x_data[i][1][0] + v2x_data[i][2]/2, v2x_data[i][1][1] + v2x_data[i][3]/2]

                                p_curr = self.database.car.position
                                curr_angle = self.database.car.direction
                                if -150 < p_parking[0] - p_curr[0] < 150:
                                    if -20 < p_parking[1] - p_curr[1] < 20:
                                        my_parking = i  # 주차공간 주변이다.
                                        if parking_direction_record == False:
                                            before_parking_x = p_curr[0]    # 주차 전위치 x
                                            before_parking_y = p_curr[1]    # 주차 전위치 y
                                            before_angle = curr_angle
                                            parking_direction_record = True
                                        break

                        if my_parking in v2x_data:
                            curr_parking = self.database.v2x_data[my_parking]
                            p_curr = self.database.car.position
                            # 현재 가야하는 주차장에대한 정보 얻음.

                            if curr_parking[4] is False:
                                # 주차 전

                                current_angle = self.database.car.direction # imu 기준
                                
                                target_angle = math.atan2(curr_parking[1][1] + self.database.v2x_data[my_parking][3]/2 - p_curr[1], curr_parking[1][0] + self.database.v2x_data[my_parking][2]/2 - p_curr[0]) * 180 / math.pi

                                # 변환
                                target_angle -= 90
                                if -270 <= target_angle <= -180:
                                    target_angle += 360

                                if current_angle - target_angle <= 8 and parking_stop is False:
                                    parking_stop = True

                                if current_angle - target_angle > 8 and parking_stop is False:
                                    self.right(8)
                                    print(1)
                                    if self.database.car.speed < 0:
                                        self.up()
                                    elif self.database.car.speed > 0:
                                        self.down()
                                    else:
                                        pass

                                elif self.database.lidar.data[90] > 15:
                                    print(2)
                                    if self.database.car.speed < 1:
                                        self.up()
                                    elif self.database.car.speed > 1:
                                        self.down()
                                    else:
                                        pass
                                
                                else:
                                    print(3)
                                    if self.database.car.speed < 0:
                                        self.up()
                                    elif self.database.car.speed > 0:
                                        self.down()
                                    else:
                                        pass

                            else:
                                # 주차 후
                                current_angle = self.database.car.direction # imu 기준
                                
                                target_angle = math.atan2(curr_parking[1][1] + self.database.v2x_data[my_parking][3]/2 - p_curr[1], curr_parking[1][0]+ self.database.v2x_data[my_parking][2]/2 - p_curr[0]) * 180 / math.pi

                                print(parking_out_done, self.database.lidar.data[179])
                                # 변환
                                target_angle -= 90
                                if -270 <= target_angle <= -180:
                                    target_angle += 360

                                if self.database.lidar.data[167] == 100:
                                    parking_out_done = True

                                if self.database.lidar.data[167] != 100 and parking_out_done is False:
                                    if self.database.car.speed < -3:
                                        self.up()
                                    elif self.database.car.speed > -3:
                                        self.down()
                                    else:
                                        pass

                                elif current_angle - before_angle < -8:
                                    self.left(8)
                                    if self.database.car.speed < 0:
                                        self.up()
                                    elif self.database.car.speed > 0:
                                        self.down()
                                    else:
                                        pass

                                else:
                                    parking_stop = False
                                    parking_out_done = False
                                    parking_direction_record = False
                                    parking_complete_list.append(my_parking)
                        # =================================================================================================================
                        
                        else:
                            # 주행
                            # ====================================================================================================================
                            lidar_data = self.database.lidar.data

                            rrr = lidar_data[20]
                            rr = lidar_data[30]
                            r = lidar_data[45]
                            m = lidar_data[90]
                            l = lidar_data[135]
                            ll = lidar_data[150]
                            lll = lidar_data[160]

                            steer_angle = 0
                            speed = 6

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

                            if steer_angle > 0:
                                self.right(steer_angle)
                                if steer_angle >= 6:
                                    speed -= 1
                            else:
                                self.left(-(steer_angle))
                                if steer_angle <= -6:
                                    speed -= 1
                            if car_stop is True:
                                speed = 0
                            
                            if self.database.car.speed < speed:
                                self.up(CAR_SPEED_CH)
                            elif self.database.car.speed > speed:
                                self.down(CAR_SPEED_CH)
                            else:
                                pass
                            # ===================================================================================================================
                        
                    else:
                        # 신호등
                        # ===================================================================================================================
                        v2x_data = self.database.v2x_data
                        my_crosswalk = 0
                        for i in v2x_data:
                            if v2x_data[i][0] == 'Crosswalk':
                                if i in complete_list:
                                    continue
                                p_crosswalk = v2x_data[i][2]
                                p_curr = self.database.car.position

                                if -60 < p_crosswalk[0] - p_curr[0] < 60:
                                    if -50 < p_crosswalk[1] - p_curr[1] < 50: # 만약 신호등이 근처에 있다면
                                        my_crosswalk = i  # 우리가 보는 신호등이다.
                                        break

                        # 현재 신호등의 정보
                        if my_crosswalk in v2x_data:
                            curr_crosswalk = self.database.v2x_data[my_crosswalk]
                            # 현재 보고 있는 신호등 까지 구함.
                            
                            if my_crosswalk not in determine_complete_list:
                                if curr_crosswalk[1] == 'green':
                                    if curr_crosswalk[5] > 0.4*curr_crosswalk[6]:   # 충분한 시간이 남았을때, 통과
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = True
                                    determine_complete_list.append(my_crosswalk)

                                elif curr_crosswalk[1] == 'red':
                                    if curr_crosswalk[5] < 1:     # 빨간 불이 곧 끝남
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = True
                                    determine_complete_list.append(my_crosswalk)

                            else:
                                if curr_crosswalk[1] == 'green' :
                                    if curr_crosswalk[5] < 0.4*curr_crosswalk[6]:   # 계속 멈춰있어라.
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = False
                                        complete_list.append(my_crosswalk)
                                        time.sleep(0.001)

                                elif curr_crosswalk[1] == 'red':
                                    if curr_crosswalk[5] > 1:                       # 초록 신호로 바뀌기 직전
                                        pass
                                    else:
                                        # 멈춤
                                        car_stop = False
                                        complete_list.append(my_crosswalk)
                                        time.sleep(0.001)
                                
                            # 멈춰야하는지, 통과해야하는지 판단함.
                            #print(car_stop, complete_list, curr_crosswalk)
                        else:
                            pass

                        # ====================================================================================================================
                        
                        # 주행
                        # ====================================================================================================================
                        lidar_data = self.database.lidar.data

                        rrr = lidar_data[20]
                        rr = lidar_data[30]
                        r = lidar_data[45]
                        m = lidar_data[90]
                        l = lidar_data[135]
                        ll = lidar_data[150]
                        lll = lidar_data[160]

                        steer_angle = 0
                        speed = CAR_SPEED

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

                        if steer_angle > 0:
                            self.right(steer_angle)
                            if steer_angle >= 6:
                                speed -= 1
                        else:
                            self.left(-(steer_angle))
                            if steer_angle <= -6:
                                speed -= 1
                        #print(lll, ll, l, r, rr, rrr, steer_angle, speed)
                        if car_stop is True:
                            speed = 0
                        
                        if self.database.car.speed < speed:
                            self.up(CAR_SPEED_CH)
                        elif self.database.car.speed > speed:
                            self.down(CAR_SPEED_CH)
                        else:
                            pass
                        # ===================================================================================================================
                    
            

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
