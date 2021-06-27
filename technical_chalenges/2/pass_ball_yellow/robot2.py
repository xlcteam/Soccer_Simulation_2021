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
    KP_ball = 0.4
    robot_pos = data[self.name]
    robot_angle = robot_pos['orientation']
    ball_angle = angle_ball(robot_angle, x,robot_pos['x'],y,robot_pos['y'])
    d = distance(x,robot_pos['x'],y,robot_pos['y'])
    max_spd = 10
    if ball_angle > 0: 
        left_speed  = -max_spd + ball_angle * KP_ball
        right_speed= -max_spd 
    else:
        left_speed = -max_spd 
        right_speed = -max_spd - ball_angle * KP_ball
    ok = False
    if(d<0.02):
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

class MyBallPassingRobot2(RCJSoccerRobot):
    def run(self):
        time_tick = 0
        kicking_start = 0
        kick_flag = False
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()
                time_tick += 1
                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                print(time_tick)
                # Q2
                if time_tick<150:
                    left_speed , right_speed ,ok= goto_xya(-0.47,0.23,123,data,self)
                    if ball_pos['y']>0.17:
                        kick_flag = True
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<300:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,133,data,self)
                    print('xxx{}'.format(time_tick))
                    if time_tick==261:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<500:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,133,data,self)
                    print('xxx{}'.format(time_tick))
                    if time_tick==415:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<600:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,133,data,self)
                    print('xxx{}'.format(time_tick))
                    if time_tick==553:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<600:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,133,data,self)
                    print('xxx{}'.format(time_tick))
                    if time_tick==553:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<750:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,123,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==682:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<850:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,120,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==800:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<930:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,129,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==898:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >8:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1000:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,129,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==981:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >8:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1100:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,128,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1060:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1180:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,131,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1147:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1200:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,131,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1147:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1250:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,128,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1221:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1350:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,127,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1309:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1420:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,127,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1394:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1520:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,140,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1469:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1580:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,140,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1547:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1650:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,135,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1630:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1730:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,135,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1630:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1800:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,120,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1755:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                elif time_tick<1900:
                    left_speed , right_speed ,ok= goto_xya(-0.33,0.22,130,data,self)
                    print('aaaa{}'.format(time_tick))
                    if time_tick==1837:
                        kicking_start = 0
                        kick_flag = True
                        print('asssssssssssssssssssssssss')
                        
                    if kicking_start >5:
                        kick_flag = False
                    if kick_flag:
                        left_speed , right_speed = -10,-10
                        kicking_start +=1
                        print(kicking_start)
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

