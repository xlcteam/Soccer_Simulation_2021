from controller import Robot
import math
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

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
def angle_ball_f(robot_angle,x_1,x_2,y_1,y_2):
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

def goto_xya(x,y,angle_desired,robot_pos):
    KP_ball = 0.4
    robot_angle = robot_pos['orientation']
    ok = False
    ball_angle = angle_ball(robot_angle, x,robot_pos['x'],y,robot_pos['y'])
    d = distance(x,robot_pos['x'],y,robot_pos['y'])
    max_spd = 10
    if ball_angle > 0: 
        left_speed  = -max_spd + ball_angle * KP_ball
        right_speed= -max_spd 
    else:
        left_speed = -max_spd 
        right_speed = -max_spd - ball_angle * KP_ball
    ok = False=
    if(d<0.02):
        abc = math.degrees(robot_angle)-angle_desired
        left_speed  = -max_spd * 0.02 *abc
        right_speed= max_spd * 0.02 *abc
        if(abs(abc)<0.1):
            ok = True
        else:
            ok = False

    left_speed = max(left_speed,-10)
    left_speed = min(left_speed,10)
    right_speed = max(right_speed,-10)
    right_speed = min(right_speed,10)
    return left_speed, right_speed,ok

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



class MyScoringRobot(RCJSoccerRobot):
    def run(self):
        finding = False
        kick = False
        goling = False
        atacing_blue = True
        while self.robot.step(TIME_STEP) != -1:
            # Get the position of our robot
            robot_pos = self.get_posfrom_devices()
            # Get lidar ranges in an array indexed 0..359, index 0 = front, 90-1 = right, 180-1 = back, 270-1 = left
            lidar_ranges = self.lidar.getRangeImage()
            # just for experiments: print sensor values
            #print(robot_pos, 'front range:', lidar_ranges[0])

            if self.is_new_data():
                data = self.get_new_data()
               
                # Get the position of the ball
                ball_pos = data['ball']
                if atacing_blue:
                    left_speed , right_speed, ok = goto_xya(ball_pos['x']-0.1,ball_pos['y']-0.1,0,robot_pos)
                    if ok or finding :
                        finding = True
                        left_speed , right_speed =-4,-4
                        #print('ok')
                        inter_x,inter_y=line_intersection(((robot_pos['x'],robot_pos['y']),(ball_pos['x'],ball_pos['y'])), ((0.85,-5),(0.85,5)))
                        distance_calc = distance(inter_x,robot_pos['x'],inter_y,robot_pos['y'])
                        angle_ball = math.degrees(math.atan2(robot_pos['y'] - ball_pos['y'],robot_pos['x'] -ball_pos['x']))
                        if angle_ball<0:
                            angle_ball += 360
                        angle_ball+=90
                        angle_ball = int(angle_ball)
                        if angle_ball>360 or angle_ball<0:
                            angle_ball = 0
                        c_index = abs(distance_calc-lidar_ranges[angle_ball]) + abs(distance_calc-lidar_ranges[angle_ball+1]) + abs(distance_calc-lidar_ranges[angle_ball+2]) + abs(distance_calc-lidar_ranges[angle_ball-1])+abs(distance_calc-lidar_ranges[angle_ball-2])
                        
                        if(inter_y<0.2 and inter_y>-0.2 and c_index<0.2):
                            left_speed , right_speed =0,0
                            kick = True
                        #print(angle_ball)
                        #print(inter_x,inter_y)
                    
                    if kick:
                        abc = angle_ball_f(robot_pos['orientation'],robot_pos['x'],ball_pos['x'],robot_pos['y'],ball_pos['y'])
                        left_speed  = 10 * 0.02 *abc
                        right_speed= -10 * 0.02 *abc
                        if abs(abc)<0.01:
                            goling = True
                    if goling:
                        left_speed , right_speed = 10,10
                    if ball_pos['x']>0.1:
                        goling = False
                        atacing_blue = False
                        left_speed , right_speed, ok = goto_xya(0.2,0,0,robot_pos)
                            
                    if kick:
                        abc = angle_ball_f(robot_pos['orientation'],robot_pos['x'],ball_pos['x'],robot_pos['y'],ball_pos['y'])
                        left_speed  = 10 * 0.02 *abc
                        right_speed= -10 * 0.02 *abc
                        if abs(abc)<0.01:
                            goling = True
                    if goling:
                        left_speed , right_speed = 9,9
                    if ball_pos['x']>0.1:
                        goling = False
                        atacing_blue = False
                        finding = False
                        kick= False
                        left_speed , right_speed, ok = goto_xya(0.2,0,0,robot_pos)
                    if ball_pos['x']<-0.1:
                        goling = False
                        atacing_blue = True 
                        left_speed , right_speed, ok = goto_xya(-0.2,0,0,robot_pos)
                else:
                    left_speed , right_speed, ok = goto_xya(ball_pos['x']+0.1,ball_pos['y']+0.1,0,robot_pos)
                    print(ok)
                    if ok:
                        left_speed , right_speed = 0,0

                    if ok or finding :
                        print('ssdas')
                        finding = True
                        left_speed , right_speed =4,4
                        #print('ok')
                        inter_x,inter_y=line_intersection(((robot_pos['x'],robot_pos['y']),(ball_pos['x'],ball_pos['y'])), ((-0.85,-5),(-0.85,5)))
                        distance_calc = distance(inter_x,robot_pos['x'],inter_y,robot_pos['y'])
                        angle_ball = math.degrees(math.atan2(robot_pos['y'] - ball_pos['y'],robot_pos['x'] -ball_pos['x']))
                        #print(angle_ball)
 
                        angle_ball+=90
                        angle_ball = int(angle_ball)
                        print(angle_ball)
                        if angle_ball>360 or angle_ball<0:
                            angle_ball = 0
                        
                        c_index = abs(distance_calc-lidar_ranges[angle_ball]) + abs(distance_calc-lidar_ranges[angle_ball+1]) + abs(distance_calc-lidar_ranges[angle_ball+2]) + abs(distance_calc-lidar_ranges[angle_ball-1])+abs(distance_calc-lidar_ranges[angle_ball-2])
                        
                        if(inter_y<0.2 and inter_y>-0.2 and c_index<0.2):
                            left_speed , right_speed =0,0
                            kick = True
                        #print(angle_ball)
                        #print(inter_x,inter_y)
                        
                    if kick:
                        abc = angle_ball_f(robot_pos['orientation'],robot_pos['x'],ball_pos['x'],robot_pos['y'],ball_pos['y'])
                        left_speed  = 10 * 0.02 *abc
                        right_speed= -10 * 0.02 *abc
                        if abs(abc)<0.01:
                            goling = True
                    if goling:
                        left_speed , right_speed = 9,9
                    if ball_pos['x']<-0.1:
                        goling = False
                        atacing_blue = True
                        kick = False
                        finding = False
                        left_speed , right_speed, ok = goto_xya(-0.2,0,0,robot_pos)
                    if ball_pos['x']>0.1:
                        goling = False
                        atacing_blue = False
                        finding = False
                        left_speed , right_speed, ok = goto_xya(0.2,0,0,robot_pos)


                left_speed = max(left_speed,-10)
                left_speed = min(left_speed,10)
                right_speed = max(right_speed,-10)
                right_speed = min(right_speed,10)
                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_scoring_robot = MyScoringRobot(Robot())
my_scoring_robot.run()
