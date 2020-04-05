'''SIR model implementation with turtles in a custom class roing random walk
Arbitrarily chosing 5 _iterations to equal 1 day.

Have yet to implement:
- graphing the data
- SCENARIOS LIKE CLUSTERING, CENTRAL MARKET, SOCIAL DISTANCING

Things that are done:
- internal database in the form of a dictionary
- spread of the disease through infection
- change of color when infected
- people entering the removed category
- update_color to work for infected and removed
- updating status variable
- a counter for no.of days infected for each node (need to add to database)
'''

import turtle
import random
import numpy as np
import matplotlib.pyplot as plt
import time

n=0 # used for incrementing self.id
COLOR = {
    's': '#0ca6e8',
    'i': '#ff0000',
    'r': '#8c8c8c'
    }
    
class Node(turtle.Turtle):
    'My Nodes that are actually turtles, but have additional functionality, such as attributes'
    
    def __init__(self,*args,**kwargs):
        # have to declare n as global otherwise it will create a local variable
        global n
        #this command runs the __init__() of the superclass, so that all properties are respected
        super(Node,self).__init__(*args,**kwargs)
        #increment n each time new init happens
        n+=1
        #set self.id to n
        self.id = n

def nodeinit():
    '''Initialize a turtle object, send it to a random location on the grid and reveal it.
    Set turtle color depending on whether susceptible group or infected group.
    Also modifies database variable to contain a list of (node id, 's' or 'i')
    :param None: None
    :return v: turtle object with set attributes like size, shape and color
    '''
    global database
    #setting temp to status so we can decrement temp without affecting status
    temp=status
    if temp[0]>0:
        #create an invisible turtle
        v=Node(visible=False)
        v.shape('circle')
        v.penup()
        v.shapesize(1, 1)
        v.speed(0)
        #the x coordinate shouldnt fall near the middle of the screen
        #tmp = list(range(15,250-(2*infection_radius)))
        #tmp += list(range(250+(2*infection_radius), 485))
        #select a random starting x coordinate        
        #random_x=random.choice(tmp)
        #select a random starting y coordinate
        #random_y=random.choice(tmp)
        random_x=random.randint(11,489)
        random_y=random.randint(11,489)
        #make database entry
        if str(v.id) not in database.keys():
            database[str(v.id)] = [[random_x, random_y], 's', 0] #setting time infected to 0

        #send turtle to random coords
        v.goto((random_x,random_y))
        #show the turtle
        v.showturtle()
        #set susceptible turtles to blue color
        v.fillcolor('#0ca6e8') #blue for susceptible
        #decrement susceptible counter
        temp[0]-=1
        return v

    if temp[1]>0:
        #create an invisible turtle
        v=Node(visible=False)
        v.shape('circle')
        #penup so it doesnt draw a line
        v.penup()
        #scale the circle down cos its too big otherwise
        v.shapesize(1, 1)
        #speed = 0 means no animation, turtle just moves to the spot
        v.speed(0)
        #send infected turtles to the centre of the screen
        v.goto((250,250))
        #add database entry of turtle location and infected status
        if str(v.id) not in database.keys():
            database[str(v.id)] = [[250, 250], 'i', 1] #setting time infected to 1
        #make the turtle visible
        v.showturtle()
        #red color for infected
        v.fillcolor('#ff0000') #red for infected
        #decrement infected counter
        temp[1]-=1
        #return the turtle object
        return v

def advance(nodes):
    '''It is kind of a method. Advances the time step and moves everything around and performs calculations by calling other functions
    :param nodes: A list of created turtle objects which represent nodes
    :return None: Moves the location of the turtle on the screen
    '''
    global database
    for node in nodes:
        #conditional checking to ensure future movement is within boundaries 
        if node.xcor() - step_size < 0:
            lx=node.xcor()
        else:
            lx=node.xcor()-step_size
        if node.xcor() + step_size > 490:
            ux=490
        else:
            ux=node.xcor()+step_size
        if node.ycor() - step_size < 0:
            ly=node.ycor()
        else:
            ly=node.ycor()-step_size
        if node.ycor() + step_size > 490:
            uy=490
        else:
            uy=node.ycor()+step_size

        #select random integer from range to move the node
        random_x=random.randint(lx,ux)
        random_y=random.randint(ly,uy)
        new_x=random_x
        new_y=random_y
        
        #send node to randomly picked points
        node.goto((new_x,new_y))
        
        #update location for current node
        update_locations(node.id, (new_x, new_y))
        
        #check for removed population
        removed(nodes)

        #update status list
        update_status(nodes)

        #check for infections
        infection(nodes)

def update_status(nodes):
    '''Updates a list status of [s,i,r] which will be useful to plot graph and get current distribution of the population'''
    global status
    global check_simulation_over
    s,i,r=0,0,0
    for key in database.keys():
        if database[key][1] == 's':
            s += 1
        elif database[key][1] == 'i':
            i += 1
        else:
            r += 1
        
    status = [s,i,r]
    if i==0:
        check_simulation_over = True

def removed(nodes):
    '''function that ensures person stays infected for a minimum number of days and then has chance not to heal for sometime after min days
    covid 19 incubation period: 14 days
    covid 19 recovery period: 14 days
    '''
    global database
    min_count = 14 #min no. of infection days
    prob = (0,1,2,3,4,5) #60% chance of recovery every consecutive day after min_count period
    for key in database.keys():
        if database[key][2] < min_count + 1:
            continue
        else:
            rand=random.randint(0,9)
            if rand in prob:
                database[key][1] = 'r'
                update_color(nodes, int(key), 'r')

def update_locations(node_id, cords):
    '''Update the location of each node as it moves and store in locations variable'''
    global database
    for key in database.keys():
        if key == str(node_id):
            database[key][0][0]=cords[0] #x cor
            database[key][0][1]=cords[1] #y cor
            break

def infection(nodes):
    '''take nodes as input and check whether other nodes are in infection radius'''
    global database
    global status
    for key1 in database.keys():  #iterate over all nodes 
        if database[key1][1]=='i':   #if element is an infected node, establish an infection zone based on infection_radius         
            infection_zonex=(database[key1][0][0]-infection_radius,database[key1][0][0]+infection_radius)
            infection_zoney=(database[key1][0][1]-infection_radius,database[key1][0][1]+infection_radius)
            for key2 in database.keys(): #iterate over all nodes again to find susceptible nodes
                if database[key2][1]=='s': #only s ppl can be infected, not r ppl
                    if database[key2][0][0]>=infection_zonex[0] and database[key2][0][0]<=infection_zonex[1]: #check if s nodes' xcor lies in infection_zonex 
                        if database[key2][0][1]>=infection_zoney[0] and database[key2][0][1]<=infection_zoney[1]: #check if s nodes' ycor lies in infection_zoney
                            #setting probability of infection to 20%
                            choice=random.randint(0,9)
                            if choice==0 or choice==9: #if choice equals any 2 numbers out of 10 numbers (20% chance), only then infect
                                #update status variable?#
                                #update locations 's' to 'i' for that node
                                database[key2][1]='i'
                                #update color of the node
                                update_color(nodes, int(key2), 'i')

def update_color(nodes, node_id, stat):
    '''called by another function, dont call directly. 
    updates color of node as soon as it gets infected'''
    for node in nodes:
        if node.id == node_id:
            node.fillcolor(COLOR[stat])

#initializing screen
wn = turtle.Screen()
wn.screensize(500,500)
wn.setworldcoordinates(0,0,500,500)

#initialize important variables for the code
list_of_nodes = [] #list of create nodes(turtle objects)
step_size = 20 #this decides max length any node can move
population = 200 #change this
s0,i0,r0=population-1,1,0 #the starting s, i and r values
status = [s0,i0,r0]
_iteration = 0 #variable to count the number of iterations 
infection_radius = 18 #units or pixels
check_simulation_over = False #ends the simulation when 'i' hits 0

database = {} #format is {'node_id': [(x,y), 's'or'i', <time_infected>], ...}

#to create and initialize all turtles based on population variable
for _ in range(population):
    list_of_nodes.append(nodeinit()) 

#execute the program continuously
while True:
    advance(list_of_nodes)
    _iteration += 1

    # incrementing the 'infected timer'
    for key in database.keys():
        if database[key][1] == 'i':
            database[key][2] += 1
    
    print(_iteration)
    print(status)
    print('-------------------')
    #simulation over when i=0
    if check_simulation_over:
        print('Simulation over!')
        wn.bye()
        break

turtle.done()