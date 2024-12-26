import pygame
import numpy as np
import random as rd
import pandas as pd
import math
import sys
import time

def fps_counter(display):
    font = pygame.font.SysFont("Arial" , 18 , bold = True)
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    display.blit(fps_t,(0,0))

def text_print(display,text_string):
    font = pygame.font.SysFont("Arial" , 100 , bold = True)
    text = str(text_string)
    text_t = font.render(text , 1, pygame.Color("RED"))
    display.blit(text_t,(0,0))


def spawn_body(body_list,m_pos,scale,x_offset,y_offset):
    text_print(display,'Enter Mass')
    screen.blit(pygame.transform.scale(display, screen.get_size()),(0,0))
    pygame.display.update()

    mass = input('input mass:')
    #create particle with:
    #1. position
    #2. mass
    n_bodies_old = len(body_list)
    m_pos = list(m_pos)
    m_pos[0] = m_pos[0]*scale 
    m_pos[1] = m_pos[1]*scale
    body_list[str(n_bodies_old)] = {
        "pos": m_pos,
        "velocity":[0,0],
        "mass": float(mass),
        "pos_prev": [],
        "trail_colour": [rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)]
    }

def update(body_i,body_list,pos_old):
    
    n_bodies = len(body_list)

    if n_bodies > 1:
        pass
    G = 0.3
    dt= 0.1
    m_i = body_list[str(body_i)]["mass"]
    pos_i = body_list[str(body_i)]["pos"]
    vel_i = body_list[str(body_i)]["velocity"]

    trail_length = 300

    #add previous position to list for trail
    body_list[str(body_i)]["pos_prev"].append([pos_i[0],pos_i[1]])
    #remove excess data from trail
    first = body_list[str(body_i)]["pos_prev"][0]
    if len(body_list[str(body_i)]["pos_prev"]) > trail_length:
        body_list[str(body_i)]["pos_prev"].remove(first)

    accel = [0,0]
    #calculate acceleration due to other bodies.
    for body_j in range(0,n_bodies):
        if body_j != body_i:
            m_j = body_list[str(body_j)]["mass"]
            pos_j = body_list[str(body_j)]["pos"] 

            mag = np.sqrt((pos_j[0]-pos_i[0])**2+(pos_j[1]-pos_i[1])**2)
            

            accel[0] = accel[0] + ((G*m_i*m_j*(pos_j[0]-pos_i[0]))/mag**3)
            accel[1] = accel[1] + ((G*m_i*m_j*(pos_j[1]-pos_i[1]))/mag**3)

    accel[0] = accel[0]/m_i
    accel[1] = accel[1]/m_i

    if abs(accel[1]) > 3:
        if accel[1] > 0:
            sgn = 1
        else:
            sgn = -1
        accel[1] = 3*sgn
    if abs(accel[0]) > 3:
        if accel[0] > 0:
            sgn = 1
        else:
            sgn = -1
        accel[0] = 3*sgn

    vel_i[0] = vel_i[0] + accel[0]
    vel_i[1] = vel_i[1] + accel[1]
    #vel_i = [1,0.5]
    #update posn
    pos_i[0] = pos_i[0] + vel_i[0]*dt
    pos_i[1] = pos_i[1] + vel_i[1]*dt

    body_list[str(body_i)]["pos"] = pos_i
    body_list[str(body_i)]["velocity"] = vel_i

    return body_list

def run(body_list,scale):
    sim = True
    while True:
        display.fill((0,0,0))


        #display.blit(map_display,(0,0))

        

        for event in pygame.event.get():
            #event is an input of some description
            #CLose window event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #pause/unpause sim.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if sim == False:
                        sim = True
                        print('sim unpaused')
                    elif sim == True:
                        sim = False
                        print('sim paused')
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                m_pos = pygame.mouse.get_pos()
                spawn_body(body_list,m_pos,scale,x_offset,y_offset)
                print('particle spawned at: ',m_pos)
                #spawn particle
            

        #loop through bodies and update positions.
        n_bodies = len(body_list)

        pos_old = []

        #create list of current positions.
        #for body in range(0,n_bodies):
        #    pos_old.append(body_list[str(body)]["pos"])

        #Find centre of mass of all bodies
        positions_x = []
        positions_y = []
        for body in range(0,n_bodies):
            positions_x.append(body_list[str(body)]["pos"][0])
            positions_y.append(body_list[str(body)]["pos"][1])
        
        if n_bodies == 0:
            x_com = 0
            y_com = 0
        else:        
            x_com = np.mean(positions_x)
            y_com = np.mean(positions_y)

        x_offset = mid_screen[0]-x_com
        y_offset = mid_screen[1]-y_com

        for body in range(0,n_bodies):
            #update
            if sim == True:
                body_list = update(body,body_list,pos_old)

            #render
            pos = body_list[str(body)]["pos"]
            #shape = pygame.Rect(pos[0],pos[1],15,15)
            #pygame.draw.rect(display,(255,255,255),shape)

            #determine size of particle:
            mass = body_list[str(body)]["mass"]
            sz_max = 25
            sz_min = 5

            mass_max = 3000
            mass_min = 20

            dy_dx = (sz_max-sz_min)/(mass_max-mass_min)

            c_int =  sz_max - dy_dx*mass_max

            if mass < mass_min:
                size = sz_min
            elif mass > mass_max:
                size = sz_max
            else:
                size = dy_dx*mass + c_int


            
            
            
            pos_cam = [pos[0]+x_offset,pos[1]+y_offset] 
            pygame.draw.circle(display,(255,255,255),pos_cam,size)
            #render trail
            trail_length = len(body_list[str(body)]["pos_prev"])
            for t in range(0,trail_length):
                t_pos = body_list[str(body)]["pos_prev"][t]
                t_pos_cam = [t_pos[0]+x_offset,t_pos[1]+y_offset]
                t_col = body_list[str(body)]["trail_colour"]
                shape = pygame.Rect(t_pos_cam[0],t_pos_cam[1],3,3)
                pygame.draw.rect(display,t_col,shape)
                #pygame.draw.circle(display,(255,0,0),t_pos,3)
            
        #centre of mass
        #pygame.draw.circle(display,(0,0,255),[x_com,y_com],20)
        if sim == False:
            text_print(display,'Sim Paused')
        #Scale up screen
        screen.blit(pygame.transform.scale(display, screen.get_size()),(0,0))
        pygame.display.update()
        #Force game to run at X FPS
        clock.tick(60)




pygame.init()

pygame.display.set_caption('n body problem')

# resolution of window
x_window = 700
y_window = 700

#scale of game. >1 means smaller pixels, <1 means bigger pixels
scale = 2


x_res = int(x_window*scale)
y_res = int(y_window*scale)

mid_screen =[x_res/2,y_res/2]

screen = pygame.display.set_mode((x_window,y_window))

        # To scale up the screen we render at a smaller size then scale it up.
        #Create a black box with 320,240 size.
display = pygame.Surface((x_res,y_res))

        #self.particle = Particle(self,(1,1),)

        #set max FPS
clock = pygame.time.Clock()


body_list = {}
camera = [0,0]
map = np.zeros([x_res,y_res], dtype=int)

run(body_list,scale)