import pygame
import sys
import random
import math
import priority_dict
from queue import PriorityQueue
from init import priority_dict

pygame.display.set_caption("Dijstra Path Planning Algorithm")


width=600
height=600
rows=30
column=30
grid=[]
obs=[]
queue=[]
path=[]
box_width=width//rows
box_height=height//column
goal_found=False
window = pygame.display.set_mode((width,height))
background_colour = (255,255,255)
window.fill(background_colour)

class Box:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.start=False
        self.wall=False
        self.goal=False
        self.queued=False
        self.visited=False
        self.neighbour=[]
        # self.dist=dist
        self.cost={}

    def draw(self,window,color):
        pygame.draw.rect(window,color,(self.x*box_width, self.y*box_height,box_width -2,box_height-2))

    def set_neighbours(self):
        if i>0:
           self.neighbour.append(grid[i-1][j])
        if i<rows-1:
           self.neighbour.append(grid[i+1][j])
    
        if j>0:
           self.neighbour.append(grid[i][j-1])
        if j<column-1:
           self.neighbour.append(grid[i][j+1])

    def hv(self):
        gx=25
        gy=28
        self.dist=math.dist([self.x,self.y],[gx,gy])


#create grid
for i in range(column):
    arr=[]
    for j in range(rows):
        # grid[i][j].neighbours()
        arr.append(Box(i,j))
    grid.append(arr)

for i in range(0,rows):
    for j in range(0,column):
        grid[i][j].set_neighbours()

start_box=grid[0][0] #intialising start point
start_box.start = True
goal_box=grid[15][28] #intialising end point
goal_box.goal = True
queue.append(start_box)



for i in range (0,100): #generating obstacles using random function
    m=random.randint(2,26)
    n=random.randint(2,26)
    block=grid[m][n]
    # obs.append(m,n)
    block.wall=True


# main
while True:
    searching=True
    begin_search=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
   
    
    if begin_search:
        if len(queue)>0 and searching:
            print(3)
            current=queue.pop(0)
            current.visited=True
            if (current==goal_box):
                begin_search=False
                searching=False
                while current.prior != start_box:
                        path.append(current.prior)
                        current = current.prior
            else:
                for nb in current.neighbour:
                    print(1)
                    if not nb.queued and not nb.wall:
                        nb.queued=True
                        nb.prior=current
                        queue.append(nb)
                        if (nb==goal_box):
                           begin_search=False
                           searching=False
    # else:
    #     print("Goal not found")
    window.fill((0,0,0))

    for i in range (column):
        for j in range(rows):
            goal_box.wall=False
            box=grid[i][j]
            box.draw(window,(50,50,50))
            if box.queued:
                box.draw(window, (200, 0, 0))

            if box.visited:
                box.draw(window, (0, 200, 0))
            if box in path:
                box.draw(window, (0, 0, 200)) 
            if box.start:
                box.draw(window,(0,200,200))
            if box.goal:
                box.draw(window,(200,200,0))
            if box.wall:
                box.draw(window,(80,80,80))
            
                
    pygame.display.flip()



