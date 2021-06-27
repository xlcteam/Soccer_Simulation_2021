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
def distance(x_1,x_2,y_1,y_2):
    a = ((x_1-x_2)*(x_1-x_2))+((y_1-y_2)*(y_1-y_2))
    return math.sqrt(a)
stop_counter = 0

class MyScoringRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                robot_angle = robot_pos['orientation']

                # YOUR CODE HERE

                r_shift =  0.12
                KP_ball = 0.4
                KP_ball_near = 0.4
                KP_goal_centring = 10
                ball_shift = 0.12
                ball_shift_lr = 0.12
                down_shift_tolerance = 0.05
                goal_position_x = 0.75 
                goal_position_y = 0
                max_spd = 10 
                
                #Ball
                ball_goal_angle = math.degrees(math.atan((ball_pos['y'])/(ball_pos['x']-0.73)))
                if ball_goal_angle > 0:     
                    ball_goal_angle = 90-ball_goal_angle
                else:
                    ball_goal_angle = -(90+ball_goal_angle)
                #print(ball_goal_angle)
                
                a_shift = math.sin(math.radians(ball_goal_angle))* r_shift #y
                b_shift = math.cos(math.radians(ball_goal_angle))* r_shift #x
                #print(a_shift,b_shift)
                ball_x = 0
                ball_y = 0 
                
                if robot_pos['x']-down_shift_tolerance>ball_pos['x']:
                    #robot nad loptou
                    if ball_pos['y']>0:
                        ball_x = ball_pos['x']
                        ball_y = ball_pos['y']-ball_shift_lr
                    else:
                        ball_x = ball_pos['x']
                        ball_y = ball_pos['y']+ball_shift_lr
                    #print('nad')
                else:
                    #robot je pod loptou
                    #print('pod')
                    if ball_pos['x'] > 0:
                        if ball_pos['y'] >0:
                            #right up
                            ideal_ball_x = ball_pos['x']+a_shift
                            ideal_ball_y = ball_pos['y']+b_shift
                        else:
                            #left up
                            ideal_ball_x = ball_pos['x']-a_shift
                            ideal_ball_y = ball_pos['y']-b_shift
                    else:
                        if ball_pos['y'] > 0:
                            #right down
                            ideal_ball_x = ball_pos['x']+a_shift
                            ideal_ball_y = ball_pos['y']+b_shift
                        else:
                            #left down
                            ideal_ball_x = ball_pos['x']-a_shift
                            ideal_ball_y = ball_pos['y']-b_shift
                           
                    ball_x = ideal_ball_x
                    ball_y = ideal_ball_y
                #smerovi vector
                s_x = robot_pos['x'] - ball_pos['x']
                s_y = robot_pos['y'] - ball_pos['y']
                #normalovi vector
                n_x = s_y
                n_y = s_x * -1
                #vseobecne vijadrenie priamky
                c = (n_x * ball_pos['x'] + n_y * robot_pos['y']) * -1
                
                v = abs(n_x * goal_position_x + n_y * goal_position_y + c) 
                v = v/(math.sqrt(n_x*n_x + n_y*n_y))
                if robot_pos['x']> ball_pos['x']:
                    v = 100
                #print(v)
                
                
                ball_angle = angle_ball(robot_angle, ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                ball_distance = distance(ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                print(robot_angle)
                
                if(ball_pos['x']<0.2):
                    if v > 0.1:
                        if ball_angle > 0: 
                            left_speed  = -max_spd + ball_angle * KP_ball
                            right_speed= -max_spd 
                        else:
                            left_speed = -max_spd 
                            right_speed = -max_spd - ball_angle * KP_ball
                    else:
                        atack = True
                        #print('point')
                        ball_angle = angle_ball(robot_angle, ball_pos['x'],robot_pos['x'],ball_pos['y'],robot_pos['y'])
                        if ball_angle > 0: 
                            left_speed  = -max_spd + ball_angle * KP_ball_near
                            right_speed= -max_spd 
                        else:
                            left_speed = -max_spd 
                            right_speed = -max_spd - ball_angle * KP_ball_near
                        #left_speed = 0 
                        #right_speed = 0
                            
                        if robot_pos['x']<0:
                            #napravo
                            left_speed = left_speed + (v * KP_goal_centring)
                        else:
                            #nalavo
                            right_speed = right_speed + (v * KP_goal_centring)
                else:
                    ball_angle = angle_ball(robot_angle, -0.1,robot_pos['x'],0,robot_pos['y'])
                    if distance(-0.1,robot_pos['x'],0,robot_pos['y'])<0.05:
                            left_speed = 0 
                            right_speed = 0
                    else:     
                        if ball_angle > 0: 
                            left_speed  = -max_spd + ball_angle * KP_ball
                            right_speed= -max_spd 
                        else:
                            left_speed = -max_spd 
                            right_speed = -max_spd - ball_angle * KP_ball
                    #print(v * KP_goal_centring)
                # Set the speed to motors
                left_speed = max(left_speed,-10)
                left_speed = min(left_speed,10)
                right_speed = max(right_speed,-10)
                right_speed = min(right_speed,10)
                #print(robot_pos['x'])
                
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

my_scoring_robot = MyScoringRobot(Robot())
my_scoring_robot.run()
