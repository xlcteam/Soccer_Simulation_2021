from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import math

TIME_STEP = 64

def angle_ball(robot_angle,x_1,x_2,y_1,y_2):
    angle = math.degrees(math.atan2(y_1 - y_2,x_1 - x_2))
    angle = angle + 180
    rotation = math.degrees(robot_angle)+90
    if rotation < 0:
        rotation += 360
    angle += rotation
    if  angle  > 360:
        angle -= 360
    angle -= 360   
    angle *= -1
    if angle>180:
        angle -=360
    return angle
def distance(x_1,x_2,y_1,y_2):
    a = ((x_1-x_2)*(x_1-x_2))+((y_1-y_2)*(y_1-y_2))
    return math.sqrt(a)

def goto_xya(x,y,angle_desired,data,self):
    KP_ball = 0.2
    robot_pos = data[self.name]
    robot_angle = robot_pos['orientation']
    ball_angle = angle_ball(robot_angle, x,robot_pos['x'],y,robot_pos['y'])
    d = distance(x,robot_pos['x'],y,robot_pos['y'])
    max_spd = 5
    if ball_angle > 0: 
        left_speed  = -max_spd + ball_angle * KP_ball
        right_speed= -max_spd 
    else:
        left_speed = -max_spd 
        right_speed = -max_spd - ball_angle * KP_ball
    ok = False
    if(d<0.001):
        abc = math.degrees(robot_angle)-angle_desired
        left_speed  = -max_spd * 0.01 *abc
        right_speed= max_spd * 0.01 *abc
        if(abc<0.002):
            ok = True
        else:
            ok = False

            

    left_speed = max(left_speed,-10)
    left_speed = min(left_speed,10)
    right_speed = max(right_speed,-10)
    right_speed = min(right_speed,10)
    return left_speed, right_speed,ok

class MyBallPassingRobot1(RCJSoccerRobot):
    def run(self):
        kicking_start = 0
        kick_flag = False
        time_tick = 0
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                #Q4
                data = self.get_new_data()
                time_tick += 1
                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                if time_tick < 200:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-54.8,data,self)
                    if time_tick == 143:
                        kick_flag = True
                        print('asd')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick < 400:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 342:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick < 520:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 481:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <650:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 620:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <700:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 620:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <780:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 740:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <900:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-52,data,self)
                    if time_tick == 857:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1000:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 941:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1080:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-47,data,self)
                    if time_tick == 1024:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1150:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-47,data,self)
                    if time_tick == 1107:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1230:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-46,data,self)
                    if time_tick == 1181:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1290:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-46,data,self)
                    if time_tick == 1264:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1370:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-52,data,self)
                    if time_tick == 1354:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1460:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 1433:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1550:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 1510:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1600:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-45,data,self)
                    if time_tick == 1585:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1750:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-55,data,self)
                    if time_tick == 1697:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick <1900:
                    left_speed , right_speed ,ok= goto_xya(0.30,-0.22,-50,data,self)
                    if time_tick == 1800:
                        kick_flag = True
                        kicking_start = 0
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)


                
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

