import pygame
import sys
# from tkinter import messagebox, Tk
import random
import math
# import priority_dict
# from queue import PriorityQueue
# from init import priority_dict
import heapdict

pygame.display.set_caption("A* Path Planning Algorithm")

width=600
height=600
rows=30
column=30
grid=[]
obs=[]
# queue=[]
queue = heapdict.heapdict()
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
        self.diagonal=False
        self.neighbour=[]
        self.dist=1
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
        
        if self.x+1<=column-1 and self.y+1<=rows-1:
            grid[self.x+1][self.y+1].diagonal=True
            self.neighbour.append(grid[self.x+1][self.y+1])
        if self.x+1<=column-1 and self.y-1>0:
            grid[self.x+1][self.y-1].diagonal=True
            self.neighbour.append(grid[self.x+1][self.y-1])
        if self.x-1>0 and self.y+1<=rows-1:
            grid[self.x-1][self.y+1].diagonal=True
            self.neighbour.append(grid[self.x-1][self.y+1])
        if self.x-1>0 and self.y-1>0:
            grid[self.x-1][self.y-1].diagonal=True
            self.neighbour.append(grid[self.x-1][self.y-1])

    def hv(self):
        gx=25
        gy=16

        if not self.diagonal:
            self.dist=math.dist([self.x,self.y],[gx,gy])
        else:
            self.dist=0.5+math.dist([self.x,self.y],[gx,gy])



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
goal_box=grid[25][16] #intialising end point
goal_box.goal = True
queue[start_box]=0



for i in range (0,100): #generating obstacles using random function
    m=random.randint(2,26)
    n=random.randint(2,26)
    block=grid[m][n]
    # obs.append(m,n)
    block.wall=True


# main
flag=0
while True:
    searching=True
    begin_search=True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in range(0,rows):
        for j in range(0,column):
            grid[i][j].hv()
   
    if begin_search:
        print()
        if len(queue.items())>0 and searching:
            print("1")
            (current, dist) = queue.peekitem()
            queue.popitem()
            current.visited=True
            if (current==goal_box):
                searching=False
                begin_search=False
                print("2")
                while current.prior != start_box:
                    path.append(current.prior)
                    current = current.prior
            else:
                for nb in current.neighbour:
                    if begin_search:
                        print("3")
                        if not nb.queued and not nb.wall and not flag:
                            nb.queued=True
                            nb.prior=current
                            queue[nb]= nb.dist
                            print("4")
                            if (nb==goal_box):
                                begin_search=False
                                print("5")
                                flag=1

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
                box.draw(window,(70,80,80))
            
                
    pygame.display.flip()
