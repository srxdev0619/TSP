import pygame 
from math import *
from random import *
from copy import *
import time

num_nodes = int(raw_input("Please enter the number of nodes to be visited: "))


#Initialize game
pygame.init()

# Set the height and width of the screen
size = [1000, 1000]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Traveling salesman problem")

#Color definitions
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  ( 0, 0, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)

coords = []
for n in range(num_nodes):
    t = (randint(0,990),randint(70,990))
    coords.append(t)
cities_pt = []

for n in range(len(coords)):
    for k in range(n+1,len(coords)):
        cities_pt.append((coords[n],coords[k]))


def draw_nodes(num_nodes,temp):
    screen.fill(WHITE)
    #pygame.draw.rect(screen,BLACK,[1,1,10,10])
    for n in temp:
        pygame.draw.circle(screen,BLUE,n,10)
    return

def dist(x,y,x1,y1):
    return ((x-x1)**2 + (y-y1)**2)

cities_p = {}
for n in cities_pt:
    cities_p[n] = [1.0,dist(n[0][0],n[0][1],n[1][0],n[1][1])]

#print cities_p

def path_dist(cities):
    if cities == []:
        return 0
    else:
        dist2 = 0
        for n in range(len(cities)-1):
            dist2 = dist2 + (dist(cities[n][0],cities[n][1],cities[n+1][0],cities[n+1][1]))**(0.5)
        return dist2

def draw_path(cities):
    if cities == []:
        return
    else:
        for n in range(len(cities)-1):
            pygame.draw.line(screen,RED,cities[n],cities[n+1],1)
        return

def draw_path1(cities):
    if cities == []:
        return
    else:
        for n in range(len(cities)-1):
            pygame.draw.line(screen,GREEN,cities[n],cities[n+1],1)
        return

def best_cityf(cities_p,city,alpha,beta):
    cities_v = {}
    prsum = 0
    for n in cities_p.keys():
         if city in n:
            cities_v[n] = cities_p[n]
            prsum = prsum + ((cities_p[n][0]**(alpha))*((1.0/cities_p[n][1])**(beta)))

    trd = []
    for n in cities_v.keys():
        cities_v[n] = ((cities_v[n][0]**(alpha))*((1.0/cities_v[n][1])**(beta)))/prsum
        trd.append(cities_v[n])
        #print cities_v[n]
    eta1 = random()
    sum1 = 0
    ind = 0
    for n in range(len(trd)):
        if sum1 > eta1:
            ind = n - 1
            break 
        sum1 = sum1 + trd[n]

    eta = trd[ind]

    for n in cities_v.keys():
        if cities_v[n] == eta:
            if city == n[0]:
                #print "Cities: ",cities_v
                #print "Eta: ",eta1
                #print "City: ",n[1]
                return n[1]
            else:
                #print "Cities: ",cities_v
                #print "City: ",n[0]
                return n[0]


class Ant():
    def __init__(self,cities_p,cities):
        self.cities_p = deepcopy(cities_p)
        self.cities_tr = []
        self.cities_l = deepcopy(cities)
        self.alpha = 1.0
        self.beta = 2.5

    def tour(self):
        #print self.cities_l
        fcity = self.cities_l[randint(0,len(self.cities_l)-1)]
        self.cities_l.remove(fcity)
        city = fcity
        self.cities_tr = [fcity]
        while self.cities_l != []:
            #print self.cities_l
            best_city = best_cityf(self.cities_p,city,self.alpha,self.beta)
            #print best_city
            tempdict = self.cities_p.keys()
            for n in tempdict:
                if city in n:
                    del self.cities_p[n]
            #try:
                #del self.cities_p[(city,best_city)]
            #except KeyError:
                #del self.cities_p[(best_city,city)]
            city = best_city
            self.cities_l.remove(city)
            self.cities_tr.append(city)
            #draw_path1(self.cities_tr)
        self.cities_tr.append(fcity)
        return self.cities_tr

    def update_ph(self,cities_p):
        #print cities_p
        for n in range(len(self.cities_tr)-1):
            first = self.cities_tr[n]
            second = self.cities_tr[n+1]
            if (first,second) in cities_p.keys():
                cities_p[(first,second)][0] = cities_p[(first,second)][0] + (100.0/path_dist(self.cities_tr))
            else:
                cities_p[(second,first)][0] = cities_p[(second,first)][0] + (100.0/path_dist(self.cities_tr))

    def reset_ant(self,cities_p,cities):
        self.cities_p = deepcopy(cities_p)
        self.cities_tr = []
        self.cities_l = deepcopy(cities)
        self.alpha = 1.0
        self.beta = 1.5


#Initializations
temp = deepcopy(coords)
city_num = randint(0,len(coords)-1)
city = coords[city_num]
fcity = coords[city_num]
cities_t = []
best_city = None
shall_loop = True
temp.remove(city)
myfont = pygame.font.SysFont("monospace", 15)
ACO = False
br = False
while True:
    draw_nodes(num_nodes,coords)
    dist1 = 1e10
    if shall_loop:
        for n in temp:
            if dist1 > dist(city[0],city[1],n[0],n[1]):
                dist1 = dist(city[0],city[1],n[0],n[1])
                best_city = n
            else:
                continue
        if temp != []:
            temp.remove(best_city)
        cities_t.append(city)
        city = best_city
        if temp == []:
            shall_loop = False
            #ACO = True
            cities_t.append(city)
            cities_t.append(fcity)
    if ACO:
        num_ants = int(raw_input("Please enter the number of ants you would require for ACO: "))
        Ants = []
        maxdist = 1e10
        t_end = time.time() + 30
        n1 = 0
        for n in range(int(num_nodes) + num_ants):
            Ants.append(Ant(cities_p,coords))
        for n in Ants:
        #while time.time() < t_end:
            #n = Ants[n1%(len(Ants))]
            temp = n.tour()
            n.update_ph(cities_p)
            #print cities_p
            tempd = path_dist(temp)
            #print tempd
            if tempd < maxdist:
                maxdist = tempd
                minpath = temp
                #print "ACO: ", maxdist
                #print "ACO path: ", minpath
            #n1 = n1 + 1
            #n.reset_ant(cities_p,coords)
            #time.sleep(1)
        ACO = False
        br = True
    draw_path(cities_t)
    pygame.time.wait(100)
    d = path_dist(cities_t)
    #print "Greedy Path: ", cities_t
    distance_label = myfont.render(("Distance Travelled by Greedy Algorithm (Red) = "+str(d)), 1, (0,0,0))
    screen.blit(distance_label, (250,20))
    pygame.display.flip()
    if temp == []:
        #print "Greedy Distance: ",d
        ans1 = raw_input("Shall the ACO algorithm be initialized (y or n)? ")
        if ans1 == "y":
            ACO = True
        else:
            break
    if br:
        break
print "Minimum Path calculated by the Greedy Algorithm: ",d
print "Minimum Distance calculated by the ACO Algorithm: ",maxdist

while True:
    draw_nodes(num_nodes,coords)
    draw_path(cities_t)
    draw_path1(minpath)
    pygame.time.wait(100)
    d = path_dist(cities_t)
    #print "Greedy Path: ", cities_t
    distance_label = myfont.render(("Distance Travelled by Greedy Algorithm (Red) = "+str(d)), 1, (0,0,0))
    screen.blit(distance_label, (200,20))
    distance_label1 = myfont.render(("Distance Travelled by ACO Algorithm (Green) = "+str(maxdist)), 1, (0,0,0))
    screen.blit(distance_label1, (200,40))
    pygame.display.flip()