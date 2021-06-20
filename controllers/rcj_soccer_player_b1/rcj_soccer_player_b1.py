# Warning This code is very poorly written but it works and due to the shortage time it must be enough
import math
import rcj_soccer_robot

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


class MyRobot(rcj_soccer_robot.RCJSoccerRobot):
    def run(self):
        last_x_ball = 0
        last_y_ball = 0
        lack_of_progres = 0
        while self.robot.step(rcj_soccer_robot.TIME_STEP) != -1:
            if self.is_new_data():
                atack = False
                self.name = self.robot.getName()
                data = self.get_new_data()
                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']
                robot_angle = robot_pos['orientation']
                #print(self.name)
                #print(ball_pos)
                #print(abs(ball_pos['x']-last_x_ball)+abs(ball_pos['y']-last_y_ball))
                #print(abs(ball_pos['x']-last_x_ball)+abs(ball_pos['y']-last_y_ball)<0.004)
                if(abs(ball_pos['x']-last_x_ball)+abs(ball_pos['y']-last_y_ball)<0.004):
                    lack_of_progres += 1
                else:
                    lack_of_progres = 0
                print(lack_of_progres)
                last_x_ball = ball_pos['x']
                last_y_ball = ball_pos['y']
                
                distance_to_y_goal_1 = distance(-0.75,data['Y1']['x'],0,data['Y1']['y'])
                distance_to_y_goal_2 = distance(-0.75,data['Y2']['x'],0,data['Y2']['y'])
                distance_to_y_goal_3 = distance(-0.75,data['Y3']['x'],0,data['Y3']['y'])
                golier_y_name = 'Y1' 
                if distance_to_y_goal_1<distance_to_y_goal_2 and distance_to_y_goal_1<distance_to_y_goal_3:
                    golier_y_name = 'Y1' 
                elif distance_to_y_goal_2<distance_to_y_goal_1 and distance_to_y_goal_2<distance_to_y_goal_3: 
                    golier_y_name = 'Y2'
                elif distance_to_y_goal_3<distance_to_y_goal_1 and distance_to_y_goal_3<distance_to_y_goal_2: 
                    golier_y_name = 'Y3'
                    
                     
                distance_to_b_goal_1 = distance(0.75,data['B1']['x'],0,data['B1']['y'])
                distance_to_b_goal_2 = distance(0.75,data['B2']['x'],0,data['B2']['y'])
                distance_to_b_goal_3 = distance(0.75,data['B3']['x'],0,data['B3']['y'])
                golier_b_name = 'B1'
                if distance_to_b_goal_1<distance_to_b_goal_2 and distance_to_b_goal_1<distance_to_b_goal_3:
                    golier_b_name = 'B1' 
                elif distance_to_b_goal_2<distance_to_b_goal_1 and distance_to_b_goal_2<distance_to_b_goal_3: 
                    golier_b_name = 'B2'
                elif distance_to_b_goal_3<distance_to_b_goal_1 and distance_to_b_goal_3<distance_to_b_goal_2: 
                    golier_b_name = 'B3'
                    
                if not self.name == golier_y_name and self.name[0]== 'Y':
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
                    #print(v)
                    
                    if v > 0.3:
                        atack = False
                    if v > 0.1 and not atack:
                        
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
                            
                        #print(v * KP_goal_centring)
                    # Set the speed to motors
                    left_speed = max(left_speed,-10)
                    left_speed = min(left_speed,10)
                    right_speed = max(right_speed,-10)
                    right_speed = min(right_speed,10)
                    #print(robot_pos['x'])
                    
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
                    #print(left_speed,right_speed)
                elif self.name == golier_y_name and self.name[0]== 'Y':
                    atack = False
                    KP_ball = 0.4
                    #steepness = 0.526
                    steepness = 0.8
                    max_spd = 10
                    atack = False
                    r_shift =  0.12
                    KP_ball_near = 0.4
                    KP_goal_centring = 10
                    ball_shift = 0.12
                    ball_shift_lr = 0.12
                    down_shift_tolerance = 0.05
                    goal_position_x = 0.75 
                    goal_position_y = 0
                    max_spd = 10
                    atack = False
                    ###########################if 
                    if lack_of_progres>50:
                        ball_pos['x'] = 0
                        ball_pos['y'] = 0
                    robot_goal_distance = distance(-0.85, robot_pos['x'],0,robot_pos['y'])
                    ball_goal_distance = distance(-0.85, ball_pos['x'],0,ball_pos['y'])
                    #print('momental distance')
                    #print(robot_goal_distance,ball_goal_distance)
                    #print('momental distance')
                    if ball_goal_distance < robot_goal_distance and robot_goal_distance < 0.4:
                        #print('atacking mode')
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
                        #print(v)
                        if v > 0.3:
                            atack = False
                        if v > 0.1 and not atack:
                            
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
                                
                            #print(v * KP_goal_centring)
                        # Set the speed to motors
                        left_speed = max(left_speed,-10)
                        left_speed = min(left_speed,10)
                        right_speed = max(right_speed,-10)
                        right_speed = min(right_speed,10)
                        #print(robot_pos['x'])
                        
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                        #print(left_speed,right_speed)
                    else:
                        #defense_curve
                        #-0.526* x^2 - 0.5 = y
                        fake_x = ball_pos['y']*-1
                        fake_y = ball_pos['x']*-1
                        #smerovi vector
                        s_x = 0 - fake_x 
                        s_y = 0.85 - fake_y 
                        #normalovi vector
                        n_x = s_y
                        n_y = s_x * -1
                        
                        if n_y == 0:
                            n_y = 0.000000001
                        if n_x == 0:
                            n_x = 0.000000001
                        #vseobecne vijadrenie priamky
                        c = (n_x * fake_x  + n_y *  fake_y )*-1
                        #priesecnik
                        #-0.526* x^2 - 0.5  = y
                        #(n_x/n_y *-1))(n * x + (c/(ny*-1)) = y
                        a = steepness
                        b = -((n_x/(n_y *-1)))
                        c = 0.5 - (c/(n_y*-1))
                        D = math.sqrt((b*b)-(4*a*c))
                        x_1 = (-b +D)/(2*a)
                        x_2 = (-b -D)/(2*a)
                        y_1 = steepness*(x_1*x_1)+0.5
                        y_2 = steepness*(x_2*x_2)+0.5
                        
                        distance_1 = math.sqrt(((fake_x-x_1)*(fake_x-x_1)) + ((fake_y-y_1)*(fake_y-y_1)))
                        distance_2 = math.sqrt(((fake_x-x_2)*(fake_x-x_2)) + ((fake_y-y_2)*(fake_y-y_2)))
                        if distance_1 < distance_2:
                            real_intersection_x = y_1 * -1
                            real_intersection_y = x_1 * -1
                        else:
                            real_intersection_x = y_2 * -1
                            real_intersection_y = x_2 * -1
                            
                        intersection_angle = angle_ball(robot_angle, real_intersection_x,robot_pos['x'],real_intersection_y,robot_pos['y'])
                        intersection_distance = distance(real_intersection_x,robot_pos['x'],real_intersection_y,robot_pos['y'])
                        if real_intersection_y > robot_pos['y'] :      
                            if intersection_angle > 0: 
                                    left_speed  = -max_spd + intersection_angle * KP_ball
                                    right_speed= -max_spd 
                            else:
                                left_speed = -max_spd 
                                right_speed = -max_spd - intersection_angle * KP_ball
                            #print('asdasdasd')
                            #print(left_speed,right_speed)
                        else:
                            intersection_angle += 180
                            if  intersection_angle > 180:
                                intersection_angle -= 360
                            if intersection_angle > 0: 
                                left_speed  = max_spd 
                                right_speed= max_spd - intersection_angle * KP_ball
                            else:
                                left_speed = max_spd + intersection_angle * KP_ball
                                right_speed = max_spd 
                        if intersection_distance<0.01:
                            left_speed  = 0
                            right_speed= 0
                            
                        if (left_speed == 0 and left_speed == 0):
                            stop_counter += 1
                        else:
                            stop_counter = 0
                        if stop_counter > 10:
                            left_speed = 10
                            right_speed = 10
                        if stop_counter > 12:    
                            stop_counter = 0
                        left_speed = max(left_speed,-10)
                        left_speed = min(left_speed,10)
                        right_speed = max(right_speed,-10)
                        right_speed = min(right_speed,10)
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                        #print(intersection_angle )
                elif (not self.name == golier_b_name) and self.name[0]== 'B':
                    r_shift =  0.12
                    KP_ball = 0.4
                    KP_ball_near = 0.4
                    KP_goal_centring = 10
                    ball_shift = 0.12
                    ball_shift_lr = 0.12
                    down_shift_tolerance = 0.05
                    goal_position_x = -0.75 
                    goal_position_y = 0
                    max_spd = 10
                    atack = False
                   
                    #Ball
                    ball_goal_angle = math.degrees(math.atan((ball_pos['y'])/(ball_pos['x']+0.73)))
                    if ball_goal_angle > 0:     
                        ball_goal_angle = 90-ball_goal_angle
                    else:
                        ball_goal_angle = -(90+ball_goal_angle)
                    #print(ball_goal_angle)
                    a_shift = math.sin(math.radians(ball_goal_angle))* r_shift #y
                    b_shift = math.cos(math.radians(ball_goal_angle))* r_shift #x
                    
                    ball_x = 0
                    ball_y = 0 
                        
                    if robot_pos['x']+down_shift_tolerance<ball_pos['x']:
                        #robot nad loptou
                        if ball_pos['y']<0:
                            ball_x = ball_pos['x']
                            ball_y = ball_pos['y']+ball_shift_lr
                        else:
                            ball_x = ball_pos['x']
                            ball_y = ball_pos['y']-ball_shift_lr
                    else:
                        #robot je pod loptou
                        if ball_pos['x'] > 0:
                            if ball_pos['y'] > 0:
                                #left down
                                ideal_ball_x = ball_pos['x']+a_shift
                                ideal_ball_y = ball_pos['y']+b_shift
                            else:
                                #right down
                                ideal_ball_x = ball_pos['x']-a_shift
                                ideal_ball_y = ball_pos['y']-b_shift
                        else:
                            if ball_pos['y'] > 0:
                                #top left
                                ideal_ball_x = ball_pos['x']+a_shift
                                ideal_ball_y = ball_pos['y']+b_shift
                            else:
                                ideal_ball_x = ball_pos['x']-a_shift
                                ideal_ball_y = ball_pos['y']-b_shift
                                #top right
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
                    if robot_pos['x']< ball_pos['x']:
                        v = 100
                    #print(v)
                    
                    ball_angle = angle_ball(robot_angle, ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                    ball_distance = distance(ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                    #print(v)
                    if v > 0.3:
                        atack = False
                    if v > 0.19 and not atack:
                        
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
                            
                        #print(v * KP_goal_centring)
                    # Set the speed to motors
                    left_speed = max(left_speed,-10)
                    left_speed = min(left_speed,10)
                    right_speed = max(right_speed,-10)
                    right_speed = min(right_speed,10)
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)
                    #print(left_speed,right_speed)
                elif self.name == golier_b_name and self.name[0]== 'B':
                    KP_ball = 0.4
                    
                    #steepness = -0.526
                    steepness = -0.8
                    max_spd = 10
                    atack = False
                    r_shift =  0.12
                    KP_ball_near = 0.4
                    KP_goal_centring = 10
                    ball_shift = 0.12
                    ball_shift_lr = 0.12
                    down_shift_tolerance = 0.05
                    goal_position_x = -0.75 
                    goal_position_y = 0
                    max_spd = 10 
                    if lack_of_progres>50:
                        ball_pos['x'] = 0
                        ball_pos['y'] = 0    
                    robot_goal_distance = distance(0.85, robot_pos['x'],0,robot_pos['y'])
                    ball_goal_distance = distance(0.85, ball_pos['x'],0,ball_pos['y'])
                    if ball_goal_distance < robot_goal_distance and robot_goal_distance < 0.4:
                        #print('atacking mode')
                        ball_goal_angle = math.degrees(math.atan((ball_pos['y'])/(ball_pos['x']+0.73)))
                        if ball_goal_angle > 0:     
                            ball_goal_angle = 90-ball_goal_angle
                        else:
                            ball_goal_angle = -(90+ball_goal_angle)
                        #print(ball_goal_angle)
                        a_shift = math.sin(math.radians(ball_goal_angle))* r_shift #y
                        b_shift = math.cos(math.radians(ball_goal_angle))* r_shift #x
                        
                        ball_x = 0
                        ball_y = 0 
                        
                        if robot_pos['x']+down_shift_tolerance<ball_pos['x']:
                            #robot nad loptou
                            if ball_pos['y']<0:
                                ball_x = ball_pos['x']
                                ball_y = ball_pos['y']+ball_shift_lr
                            else:
                                ball_x = ball_pos['x']
                                ball_y = ball_pos['y']-ball_shift_lr
                        else:
                            #robot je pod loptou
                            if ball_pos['x'] > 0:
                                if ball_pos['y'] > 0:
                                    #left down
                                    ideal_ball_x = ball_pos['x']+a_shift
                                    ideal_ball_y = ball_pos['y']+b_shift
                                else:
                                    #right down
                                    ideal_ball_x = ball_pos['x']-a_shift
                                    ideal_ball_y = ball_pos['y']-b_shift
                            else:
                                if ball_pos['y'] > 0:
                                    #top left
                                    ideal_ball_x = ball_pos['x']+a_shift
                                    ideal_ball_y = ball_pos['y']+b_shift
                                else:
                                    ideal_ball_x = ball_pos['x']-a_shift
                                    ideal_ball_y = ball_pos['y']-b_shift
                                    #top right
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
                        if robot_pos['x']< ball_pos['x']:
                            v = 100
                        #print(v)
                        
                        ball_angle = angle_ball(robot_angle, ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                        ball_distance = distance(ball_x,robot_pos['x'],ball_y,robot_pos['y'])
                        #print(v)
                        if v > 0.3:
                            atack = False
                        if v > 0.19 and not atack:
                            
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
                                
                            #print(v * KP_goal_centring)
                        # Set the speed to motors
                        left_speed = max(left_speed,-10)
                        left_speed = min(left_speed,10)
                        right_speed = max(right_speed,-10)
                        right_speed = min(right_speed,10)
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                        #print(left_speed,right_speed)
                    else:    
                        #-0.526* x^2 - 0.5 = y
                        fake_x = ball_pos['y']*-1
                        fake_y = ball_pos['x']*-1
                        #smerovi vector
                        s_x = 0 - fake_x 
                        s_y = -0.85 - fake_y 
                        #normalovi vector
                        n_x = s_y
                        n_y = s_x * -1
                        
                        if n_y == 0:
                            n_y = 0.000000001
                        if n_x == 0:
                            n_x = 0.000000001
                        #vseobecne vijadrenie priamky
                        c = (n_x * fake_x  + n_y *  fake_y )*-1
                        #priesecnik
                        #-0.526* x^2 - 0.5  = y
                        #(n_x/n_y *-1))(n * x + (c/(ny*-1)) = y
                        a = steepness
                        b = -((n_x/(n_y *-1)))
                        c = -0.5 - (c/(n_y*-1))
                        D = math.sqrt((b*b)-(4*a*c))
                        x_1 = (-b +D)/(2*a)
                        x_2 = (-b -D)/(2*a)
                        y_1 = steepness*(x_1*x_1)-0.5
                        y_2 = steepness*(x_2*x_2)-0.5
                        
                        distance_1 = math.sqrt(((fake_x-x_1)*(fake_x-x_1)) + ((fake_y-y_1)*(fake_y-y_1)))
                        distance_2 = math.sqrt(((fake_x-x_2)*(fake_x-x_2)) + ((fake_y-y_2)*(fake_y-y_2)))
                        if distance_1 < distance_2:
                            real_intersection_x = y_1 * -1
                            real_intersection_y = x_1 * -1
                        else:
                            real_intersection_x = y_2 * -1
                            real_intersection_y = x_2 * -1
                            
                        intersection_angle = angle_ball(robot_angle, real_intersection_x,robot_pos['x'],real_intersection_y,robot_pos['y'])
                        intersection_distance = distance(real_intersection_x,robot_pos['x'],real_intersection_y,robot_pos['y'])
                        if real_intersection_y > robot_pos['y'] :      
                            if intersection_angle > 0: 
                                    left_speed  = -max_spd + intersection_angle * KP_ball
                                    right_speed= -max_spd 
                            else:
                                left_speed = -max_spd 
                                right_speed = -max_spd - intersection_angle * KP_ball
                            #print('asdasdasd')
                            #print(left_speed,right_speed)
                        else:
                            intersection_angle += 180
                            if  intersection_angle > 180:
                                intersection_angle -= 360
                            if intersection_angle > 0: 
                                left_speed  = max_spd 
                                right_speed= max_spd - intersection_angle * KP_ball
                            else:
                                left_speed = max_spd + intersection_angle * KP_ball
                                right_speed = max_spd 
                        if intersection_distance<0.01:
                            left_speed  = 0
                            right_speed= 0
                        
                        left_speed = max(left_speed,-10)
                        left_speed = min(left_speed,10)
                        right_speed = max(right_speed,-10)
                        right_speed = min(right_speed,10)
                        if (right_speed == 0 and left_speed == 0):
                            stop_counter += 1
                        else:
                            stop_counter = 0
                        if stop_counter > 10:
                            left_speed = 10
                            right_speed = 10
                        if stop_counter > 12:    
                            stop_counter = 0
                        self.left_motor.setVelocity(left_speed)
                        self.right_motor.setVelocity(right_speed)
                        #print(intersection_angle )
                else:
                    pass
               
            
my_robot = MyRobot()
my_robot.run()
