#!/usr/bin/env python
# coding: utf-8

# In[4]:


#for score keeping - faster the time, the better

import pygame
import time
import csv
import matplotlib.pyplot as plt

print("Welcome to Alienation! Controls are simple:")
print("Press spacebar to shoot and L + R arrow keys to navigate.")
print("Clear the walls as fast as you can.")
print("Try your best not to miss, your accuracy counts :D ")
player_name = input("What's your name?\n")

#initialize the pygame
pygame.init()

def player(x,y):
    screen.blit(player_icon, (x, y)) 

#game window, width 800, height 600, 
screen = pygame.display.set_mode((800,600))

#block colours 
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
block_gray = (128,128,128)

#define game variables
cols = 6
rows = 6

screen_width = 800
screen_height = 600

total_shots = 0
total_hits = 0

#brick wall class - <<learned from <<https://www.youtube.com/watch?v=NIfkaOF3Hjs&t=5s>> ------

class wall():
    def __init__(self):
        self.width = screen_width // (cols * 2) 
        self.height = 50

    def create_wall(self):
        #responsible for literally creating the walls - e.g., the rectangles and sizing etc. 
        
        self.blocks = []
        #define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            #reset the block row list
            block_row = []
            #iterate through each column in that row
            for col in range(cols):
                #generate x and y positions for each block and create a rectangle from that
                block_x = col * 2 * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                #assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                #create a list at this point to store the rectangles and colour data
                block_individual = [rect, strength, col * 2 * self.width, "r"]
                #append that individual block to the block row
                block_row.append(block_individual)
            #append the row to the full list of blocks
            self.blocks.append(block_row)


    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #draws the wall and assigns a colour based on block strength + the positions 
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                elif block[1] == 0:
                    block_col = block_gray
                    
                #if this is at the top left corner, we only move 60 units
                #determines if direction should be swapped 
                if block[0].left == block[2] + 60:
                    block[3] = "l"
                elif block[0].left == block[2]:
                    block[3] = "r"
                #moving the blocks 
                if block[3] == "r":
                    block_change = 1
                else:
                    block_change = -1

                block[0].move_ip(block_change, 0)

                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, (0,0,0), (block[0]), 2)


#---------- start of creative aspect -------------#

#create a wall
wall = wall()
wall.create_wall()

#background 
background = pygame.image.load('ALIEN.png')

#title of game
#CSCA2_A.png was made by myself using CSP 
pygame.display.set_caption("Alienation")
icon = pygame.image.load('CSCA20_A.png')
#ensures icon has been added
pygame.display.set_icon(icon)

#player icon
player_icon = pygame.image.load('CSCA20_A.png')
playerX = 370
playerY = 480
playerX_change = 0

#laser_bullet 
#ready - you can't see laser on screen
#fire - the laser shoots out 
laser = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10 
laser_state = "ready"


#-------
#function of laser
#when we press space bar, laser is fired 

def fire_laser(x,y): 
    #calling the "ready"
    #global - can be accessed inside the function 
    #the variables are outside of the function, use global for access  
    global laser_state 
    global laserY
    global keep_going
    global total_hits
    #can access value of laser_state 
    #after pressing space 
    laser_state = "fire"
    #makes sure laser appears centered from spaceship 

    screen.blit(laser,(x + 9, y))
    
    #checks if we hit the wall (collision)
    for walls in wall.blocks:
        for block in walls:
            if block[0].collidepoint(x + 20, y) and block[1] > 0:
                total_hits += 1
                block[1] -= 1
                laser_state = "ready"
                laserY = 480

#------

#this is the beginning of the section that is learned from <<https://www.youtube.com/watch?v=FfWpgLFMI7w&t=5856s>> 

#game loop
start_time = time.time()
keep_going = True 
while keep_going: 

    #make sure background shows 
    screen.blit(background,(0,0))

    #events that are happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    # using keys to move right or left + speed 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3   
    #using space bar to fire laser 
            if event.key == pygame.K_SPACE:
                #want to make it that can only press the space bar when it's in condition
                #checks if laser is already on screen or not 
                if laser_state == "ready":
                #playerX - movement where the spaceship is the x coordinate of spaceship 
                #laser moving in the direction of the spaceship 
                #x coordinate will be saved and move separate from the spaceship 
                    total_shots += 1
                    laserX = playerX
                    fire_laser(laserX, laserY)

                #centers player and will stop moving when we stop using arrow keys
        if event.type == pygame.KEYUP: 
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                    playerX_change = 0 


    #draw wall
    wall.draw_wall()

    #laser movement 
    #laser will reset to 480 pixels of y 
    if laserY <= 0: 
        laserY = 480 
        laser_state = "ready"

    if laser_state == "fire": 
        fire_laser(laserX, laserY)
        laserY -= laserY_change 


    #player is drawn on top of the screen (order matters)
    playerX += playerX_change

    #want to make sure that it stays in frame--> using if statement 
    #stays in boundry 
    if playerX <= 0:
        playerX = 0 
    elif playerX >= 750: 
        playerX = 750  

    player(playerX,playerY)

    found_wall = False
    for walls in wall.blocks:
        for block in walls:
            if block[1] > 0:
                found_wall = True
                break

    if not found_wall:
        keep_going = False

    pygame.display.update()
#-------- end of yt tut ----------

#start of implementation of course concepts, csv, matplotlib, dictionaries, lists, 
pygame.quit()

end_time = time.time()
print("Total elapsed time in seconds is " + str(end_time - start_time))
print("Total accuracy is " + str(total_hits / total_shots * 100))

output_handle = open("stats.csv", "a", newline='')

csv_writer = csv.writer(output_handle, dialect='excel')
csv_writer.writerow([player_name, str(total_hits / total_shots * 100), str(end_time - start_time)])

output_handle.close()

name_to_accuracy = {}
name_to_time = {}

input_handle = open("stats.csv", "r")
csv_reader = csv.reader(input_handle, delimiter=',')

#all names (and repeats) will be stored in the csv file
#but only the latest scores per name are taken because it's a dictionary 
for next_row in csv_reader:
    name = next_row[0]
    accuracy = float(next_row[1])
    time = float(next_row[2])
        #what is currently inside dict is old_acc
        #if new_acc is greater than old_acc
        #new_acc becomes old_acc 
    if name not in name_to_accuracy or accuracy > name_to_accuracy[name]: 
        #old acc to new acc
        name_to_accuracy[name] = accuracy
        
    #store name bc key did not exist + same format 
    #keep lowest time 
    if name not in name_to_time or time < name_to_time[name]:
        name_to_time[name] = time 
input_handle.close()
print(name_to_accuracy)
print(name_to_time)   

#put dict into list 
#name_to_acc
#name_to_time
name_list = []
acc_list = []
time_list = []

#plotting stuff things 
for player_name in name_to_time:
    name_list.append(player_name)
    time_list.append(name_to_time[player_name])
    acc_list.append(name_to_accuracy[player_name])

plt.bar(name_list, acc_list)
plt.ylabel("the accuracy of lasers shot in percent")
plt.xlabel("Player Names")
plt.title ("The Highest Accuracy per Player")
plt.show()

plt.bar(name_list, time_list)
plt.ylabel("Fastest block clearance in secs")
plt.xlabel("Player Names")
plt.title ("The fastest time taken to clear the blocks per player")
plt.show()


# In[ ]:




