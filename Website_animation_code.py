import matplotlib.pyplot as plt
from Person import Person, Worker, Child, Key_Worker
from EnvironmentClass import Environment, House, Transport
import numpy as np 
import time
import matplotlib.animation as animation
from matplotlib.lines import Line2D



global percentage 
percentage = []

class Simulation:
    '''Defines a class for the simulation of a pandemic.'''
      
    def __init__(self,size,endtime,house_number,initial_infected,initial_building_num):
        '''Parameters:
        size: [xwidth, ywidth] size of board
        endtime: end time for simulation (is this necessary)
        house_number: number of houses in simulation
        initial_infected: number of people initially infected
        initial_building_num: initial number of buildings for workers
        '''
        
        self.size = size
        self.endtime = endtime
        self.time = 0 
        self.sim_time = 0
        self.day = 1
        self.population = 0
        self.house_number = house_number
        self.infected = initial_infected
        self.dead = 0
        self.personlist = None
        self.buildinglist = None
        self.key_buildinglist = None
        self.schoollist = None
        # Age distribution of population https://www.statista.com/statistics/281174/uk-population-by-age/
        self.age_dist =   {'yrs0-19': 0.2346032224,
                            'yrs20-44': 0.3241981629,
                            'yrs45-54': 0.1382321939,
                            'yrs55-64': 0.1198614666,
                            'yrs65-74': 0.1001355218,
                            'yrs75-84': 0.0588766752,
                            'yrs85plus':0.02409275711}
        self.initial_building_num = initial_building_num
        self.initial_building_placement()
        self.initial_key_building_placement()
        self.initial_school_placement()
        self.initial_house_placement()
        #Iterates through update cycles until end condition
        self.starttime = time.time()
        self.hour = 0
    
    def overlap(self, building_1_x, building_1_y, building_2_x, building_2_y):
        '''
        Checks if two buildings are overlapping

        Parameters
        ----------
        building_1_x : list
            x_coordinates of left and right sides of building 1.
        building_1_y : list
            y_coordinates of top and bottom simdes of building 1.
        building_2_x : list
            x_coordinates of left and right sides of building 2.
        building_2_y : list
            y_coordinates of top and bottom simdes of building 2.

        Returns
        -------
        True: if buildings overlap.
        
        False: if buildings do not overlap.

        '''
        if (building_1_x[0] < building_2_x[0] < building_1_x[1]) or (building_1_x[0] < building_2_x[1] < building_1_x[1]):
            x_match = True
        else:
            x_match = False
        if (building_1_y[0] < building_2_y[0] < building_1_y[1]) or (building_1_y[0] < building_2_y[1] < building_1_y[1]):
            y_match = True
        else:
            y_match = False
        if x_match and y_match:
            return True
        else:
            return False

    def initial_building_placement(self):
        '''Defines the placement and creation of buildings (where regular workers work) on the board'''
        # define the x & y coordinates of buildings
        building_size = [10, 10]
        x_buildings = []
        y_buildings = []
        while len(x_buildings) <= self.initial_building_num:
            x_building = np.random.uniform()*200 -100
            y_building = np.random.uniform()*200 -100
            if len(x_buildings) == 0:
                x_buildings.append(x_building)
                y_buildings.append(y_building)
            else:
                # checks if any buildings are overlapping with each other
                overlapping = False
                for building in range(len(x_buildings)):
                    if self.overlap([x_building-(building_size[0]/2), x_building+(building_size[0]/2)],
                                    [y_building-(building_size[1]/2), y_building+(building_size[1]/2)], 
                                    [x_buildings[building]-(building_size[0]/2), x_buildings[building]+(building_size[0]/2)],
                                    [y_buildings[building]-(building_size[1]/2), y_buildings[building]+(building_size[1]/2)]):
                        overlapping = True
                        break
                # only appends coordinates of house if not overlapping with any other building
                if overlapping == False:
                    x_buildings.append(x_building)
                    y_buildings.append(y_building)
                else:
                    pass
        # create buildings
        self.buildinglist = [Environment('Building'+'_'+str(i),[x_buildings[i],y_buildings[i]],building_size,0,0,5,50) for i in range(len(x_buildings))]
        
    def initial_key_building_placement(self):
        '''Defines the placement and creation of key buildings (where key workers work) on the board'''
        # define the x & y coordinates of key buildings
        key_building_size = [10, 10]
        x_key_buildings = []
        y_key_buildings = []
        while len(x_key_buildings) <= self.initial_building_num:
            x_key_building = np.random.uniform()*200 -100
            y_key_building = np.random.uniform()*200 -100
            if len(x_key_buildings) == 0:
                x_key_buildings.append(x_key_building)
                y_key_buildings.append(y_key_building)
            else:
                # checks if any key buildings are overlapping with each other
                overlapping_internal = False
                for key_building in range(len(x_key_buildings)):
                    if self.overlap([x_key_building-(key_building_size[0]/2), x_key_building+(key_building_size[0]/2)],
                                    [y_key_building-(key_building_size[1]/2), y_key_building+(key_building_size[1]/2)], 
                                    [x_key_buildings[key_building]-(key_building_size[0]/2), x_key_buildings[key_building]+(key_building_size[0]/2)],
                                    [y_key_buildings[key_building]-(key_building_size[1]/2), y_key_buildings[key_building]+(key_building_size[1]/2)]):
                        overlapping_internal = True
                        break
                # checks if any key buildings are overlapping with buildings
                overlapping_building = False
                if overlapping_internal == False:
                    for building in range(len(self.buildinglist)):
                        if self.overlap([x_key_building-(key_building_size[0]/2), x_key_building+(key_building_size[0]/2)],
                                        [y_key_building-(key_building_size[1]/2), y_key_building+(key_building_size[1]/2)], 
                                        [self.buildinglist[building].position[0]-(self.buildinglist[building].size[0]/2),
                                         self.buildinglist[building].position[0]+(self.buildinglist[building].size[0]/2)],
                                        [self.buildinglist[building].position[1]-(self.buildinglist[building].size[1]/2),
                                         self.buildinglist[building].position[1]+(self.buildinglist[building].size[1]/2)]):
                            overlapping_building = True
                            break
                # only appends coordinates of key building if not overlapping with any other building (key or not)
                if overlapping_internal == False and overlapping_building == False:
                    x_key_buildings.append(x_key_building)
                    y_key_buildings.append(y_key_building)
                else:
                    pass
        # create key buildings
        self.key_buildinglist = [Environment('KeyBuilding'+'_'+str(i),[x_key_buildings[i],y_key_buildings[i]],key_building_size,0,0,5,50) for i in range(len(x_key_buildings))]

    def initial_school_placement(self):
        '''Defines the placement and creation of schools (where children go) on the board'''
        # define the x & y coordinates of schools
        school_size = [15, 5]
        x_schools = []
        y_schools = []
        self.initial_school_num = int(self.house_number/50)
        if self.initial_school_num == 0:
            self.initial_school_num = 1
        while len(x_schools) <= self.initial_school_num:
            x_school = np.random.uniform()*200 -100
            y_school = np.random.uniform()*200 -100
            if len(x_schools) == 0:
                x_schools.append(x_school)
                y_schools.append(y_school)
            else:
                # checks if any schools are overlapping with each other
                overlapping_internal = False
                for school in range(len(x_schools)):
                    if self.overlap([x_school-(school_size[0]/2), x_school+(school_size[0]/2)],
                                    [y_school-(school_size[1]/2), y_school+(school_size[1]/2)], 
                                    [x_schools[school]-(school_size[0]/2), x_schools[school]+(school_size[0]/2)],
                                    [y_schools[school]-(school_size[1]/2), y_schools[school]+(school_size[1]/2)]):
                        overlapping_internal = True
                        break
                # checks if any schools are overlapping with buildings
                overlapping_building = False
                if overlapping_internal == False:
                    for building in range(len(self.buildinglist)):
                        if self.overlap([x_school-(school_size[0]/2), x_school+(school_size[0]/2)],
                                        [y_school-(school_size[1]/2), y_school+(school_size[1]/2)], 
                                        [self.buildinglist[building].position[0]-(self.buildinglist[building].size[0]/2),
                                         self.buildinglist[building].position[0]+(self.buildinglist[building].size[0]/2)],
                                        [self.buildinglist[building].position[1]-(self.buildinglist[building].size[1]/2),
                                         self.buildinglist[building].position[1]+(self.buildinglist[building].size[1]/2)]):
                            overlapping_building = True
                            break
                # checks if any schools are overlapping with key buildings
                overlapping_key_building = False
                if overlapping_internal == False and overlapping_building == False:
                    for key_building in range(len(self.key_buildinglist)):
                        if self.overlap([x_school-(school_size[0]/2), x_school+(school_size[0]/2)],
                                        [y_school-(school_size[1]/2), y_school+(school_size[1]/2)], 
                                        [self.key_buildinglist[key_building].position[0]-(self.key_buildinglist[key_building].size[0]/2),
                                         self.key_buildinglist[key_building].position[0]+(self.key_buildinglist[key_building].size[0]/2)],
                                        [self.key_buildinglist[key_building].position[1]-(self.key_buildinglist[key_building].size[1]/2),
                                         self.key_buildinglist[key_building].position[1]+(self.key_buildinglist[key_building].size[1]/2)]):
                            overlapping_key_building = True
                            break
                # only appends coordinates of school if not overlapping with any building (key or not) or school
                if overlapping_internal == False and overlapping_building == False and overlapping_key_building == False:
                    x_schools.append(x_school)
                    y_schools.append(y_school)
                else:
                    pass
                    # create schools
        self.schoollist = [Environment('School'+'_'+str(i),[x_schools[i],y_schools[i]],school_size,0,0,5,50) for i in range(len(x_schools))]

    def initial_house_placement(self):
        '''Defines the placement and creation of houses (and thus of people within them) on the board'''
        # define the x & y coordinates of houses
        house_size = [5, 5]
        x_houses = []
        y_houses = []
        while len(x_houses) <= self.house_number:
            x_house = np.random.uniform()*200 -100
            y_house = np.random.uniform()*200 -100
            if len(x_houses) == 0:
                x_houses.append(x_house)
                y_houses.append(y_house)
            else:
                # checks if any houses are overlapping
                overlapping_internal = False
                for house in range(len(x_houses)):
                    if self.overlap([x_house-(house_size[0]/2), x_house+(house_size[0]/2)],
                                    [y_house-(house_size[1]/2), y_house+(house_size[1]/2)], 
                                    [x_houses[house]-(house_size[0]/2), x_houses[house]+(house_size[0]/2)],
                                    [y_houses[house]-(house_size[1]/2), y_houses[house]+(house_size[1]/2)]):
                        overlapping_internal = True
                        break
                # checks if any houses are overlapping with buildings
                overlapping_building = False
                if overlapping_internal == False:
                    for building in range(len(self.buildinglist)):
                        if self.overlap([x_house-(house_size[0]/2), x_house+(house_size[0]/2)],
                                        [y_house-(house_size[1]/2), y_house+(house_size[1]/2)], 
                                        [self.buildinglist[building].position[0]-(self.buildinglist[building].size[0]/2),
                                         self.buildinglist[building].position[0]+(self.buildinglist[building].size[0]/2)],
                                        [self.buildinglist[building].position[1]-(self.buildinglist[building].size[1]/2),
                                         self.buildinglist[building].position[1]+(self.buildinglist[building].size[1]/2)]):
                            overlapping_building = True
                            break
                # checks if any houses are overlapping with key buildings
                overlapping_key_building = False
                if overlapping_internal == False and overlapping_building == False:
                    for key_building in range(len(self.key_buildinglist)):
                        if self.overlap([x_house-(house_size[0]/2), x_house+(house_size[0]/2)],
                                        [y_house-(house_size[1]/2), y_house+(house_size[1]/2)], 
                                        [self.key_buildinglist[key_building].position[0]-(self.key_buildinglist[key_building].size[0]/2),
                                         self.key_buildinglist[key_building].position[0]+(self.key_buildinglist[key_building].size[0]/2)],
                                        [self.key_buildinglist[key_building].position[1]-(self.key_buildinglist[key_building].size[1]/2),
                                         self.key_buildinglist[key_building].position[1]+(self.key_buildinglist[key_building].size[1]/2)]):
                            overlapping_key_building = True
                            break
                # checks if any houses are overlapping with schools
                overlapping_school = False
                if overlapping_internal == False and overlapping_building == False and overlapping_key_building == False:
                    for school in range(len(self.schoollist)):
                        if self.overlap([x_house-(house_size[0]/2), x_house+(house_size[0]/2)],
                                        [y_house-(house_size[1]/2), y_house+(house_size[1]/2)], 
                                        [self.schoollist[school].position[0]-(self.schoollist[school].size[0]/2),
                                         self.schoollist[school].position[0]+(self.schoollist[school].size[0]/2)],
                                        [self.schoollist[school].position[1]-(self.schoollist[school].size[1]/2),
                                         self.schoollist[school].position[1]+(self.schoollist[school].size[1]/2)]):
                            overlapping_school = True
                            break
                # only appends coordinates of house if not overlapping with any other structure
                if overlapping_internal == False and overlapping_building == False and overlapping_key_building == False and overlapping_school == False:
                    x_houses.append(x_house)
                    y_houses.append(y_house)
                else:
                    pass
        # randomly assign number of people in houses
        people_counters = np.random.randint(1,5, self.house_number)
        # some houses have all their initial inhabitants infected
        initially_infected = np.append(people_counters[:self.infected], np.zeros(self.house_number-self.infected))
        # create houses
        self.houselist = [House('House'+'_'+str(i),[x_houses[i],y_houses[i]],house_size,people_counters[i],initially_infected[i],2,1,self.buildinglist, self.key_buildinglist, self.schoollist) for i in range(self.house_number)]
        # list of people with inhabitants of each house
        self.personlist = []
        for house in self.houselist:
          self.personlist.extend(house.house_personlist)
        self.population = len(self.personlist) # total pop.
  
    def info(self):
        print('Day: {}'.format(self.day))
        print('Time: {}'.format(self.hour))


    def update(self):
        '''Method for updating the simulation at each turn'''
        self.state = []
        position_list = []
        infected_list = []
        for person in self.personlist:
            person.update(self.hour,self.day)
            position_list.append((person.position[0],person.position[1]))
            infected_list.append(person.infection_status)
        if self.hour < 23:
            self.hour +=1
        elif self.hour == 23:
            self.hour = 0
        if self.hour == 0:
            if self.day <= 7:
                self.day += 1
            elif self.day == 8:
                self.day = 1
        self.state.append(np.array(position_list))
        self.state.append(np.array(infected_list))
    


#
#fig = plt.figure()
#fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
#                     xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))
#
## particles holds the locations of the particles
#particles = ax.scatter([], [], c=[],s=30, cmap="bwr")
#
#
#bounds = [-120, 120, -120, 120]
## rect is the box edge
#rect = plt.Rectangle(bounds[::2],
#                     bounds[1] - bounds[0],
#                     bounds[3] - bounds[2],
#                     ec='none', lw=2, fc='none')
#ax.add_patch(rect)
#def init():
#    """initialize animation"""
#    print('init animation func')
#    global sim, rect
#    sim = Simulation([50, 50], 10, 300, 20, 50)
#    rect.set_edgecolor('k')
#    proxy = []
#    # plotting houses
#    house_centre_points = [sim.houselist[i].position for i in range(len(sim.houselist))]
#    house_edges = [[house_centre_points[i][0]+(sim.houselist[i].size[0]/2),
#                    house_centre_points[i][1]+(sim.houselist[i].size[1]/2),
#                    house_centre_points[i][0]-(sim.houselist[i].size[0]/2),
#                    house_centre_points[i][1]-(sim.houselist[i].size[1]/2)] 
#                   for i in range(len(sim.houselist))]
#    houses = [plt.Rectangle([house_centre_points[i][0]-(sim.houselist[i].size[0]/2),
#                             house_centre_points[i][1]-(sim.houselist[i].size[1]/2)],
#                            house_edges[i][0] - house_edges[i][2],
#                            house_edges[i][1] - house_edges[i][3],
#                            color='green', alpha=0.2) for i in range(len(sim.houselist))]    
#    proxy.append(plt.Rectangle([0, 0], sim.houselist[0].size[0], sim.houselist[0].size[1], color='green', alpha=0.2))
#    for house in houses:
#        ax.add_patch(house)
#    # plotting buildings
#    building_centre_points = [sim.buildinglist[i].position for i in range(len(sim.buildinglist))]
#    building_edges = [[building_centre_points[i][0]+(sim.buildinglist[i].size[0]/2),
#                       building_centre_points[i][1]+(sim.buildinglist[i].size[1]/2),
#                       building_centre_points[i][0]-(sim.buildinglist[i].size[0]/2),
#                       building_centre_points[i][1]-(sim.buildinglist[i].size[1]/2)] 
#                      for i in range(len(sim.buildinglist))]
#    buildings = [plt.Rectangle([building_centre_points[i][0]-(sim.buildinglist[i].size[0]/2),
#                                building_centre_points[i][1]-(sim.buildinglist[i].size[1]/2)],
#                               building_edges[i][0] - building_edges[i][2],
#                               building_edges[i][1] - building_edges[i][3],
#                               color='black', alpha=0.2) for i in range(len(sim.buildinglist))]
#    proxy.append(plt.Rectangle([0, 0], sim.buildinglist[0].size[0], sim.buildinglist[0].size[1], color='black', alpha=0.2))
#    for building in buildings:
#        ax.add_patch(building)
#    # plotting key buildings
#    key_building_centre_points = [sim.key_buildinglist[i].position for i in range(len(sim.key_buildinglist))]
#    key_building_edges = [[key_building_centre_points[i][0]+(sim.key_buildinglist[i].size[0]/2),
#                           key_building_centre_points[i][1]+(sim.key_buildinglist[i].size[1]/2),
#                           key_building_centre_points[i][0]-(sim.key_buildinglist[i].size[0]/2),
#                           key_building_centre_points[i][1]-(sim.key_buildinglist[i].size[1]/2)]
#                          for i in range(len(sim.key_buildinglist))]
#    key_buildings = [plt.Rectangle([key_building_centre_points[i][0]-(sim.key_buildinglist[i].size[0]/2),
#                                    key_building_centre_points[i][1]-(sim.key_buildinglist[i].size[1]/2)],
#                                   key_building_edges[i][0] - key_building_edges[i][2],
#                                   key_building_edges[i][1] - key_building_edges[i][3],
#                                   color='#fdd0ff', alpha=0.2) for i in range(len(sim.key_buildinglist))]
#    proxy.append(plt.Rectangle([0, 0], sim.key_buildinglist[0].size[0], sim.key_buildinglist[0].size[1],
#                               color='#fdd0ff', alpha=0.2))
#    for key_building in key_buildings:
#        ax.add_patch(key_building)
#    # plotting schools
#    school_centre_points = [sim.schoollist[i].position for i in range(len(sim.schoollist))]
#    school_edges = [[school_centre_points[i][0]+(sim.schoollist[i].size[0]/2),
#                     school_centre_points[i][1]+(sim.schoollist[i].size[1]/2),
#                     school_centre_points[i][0]-(sim.schoollist[i].size[0]/2),
#                     school_centre_points[i][1]-(sim.schoollist[i].size[1]/2)] for i in range(len(sim.schoollist))]
#    schools = [plt.Rectangle([school_centre_points[i][0]-(sim.schoollist[i].size[0]/2),
#                              school_centre_points[i][1]-(sim.schoollist[i].size[1]/2)],
#                             school_edges[i][0] - school_edges[i][2],
#                             school_edges[i][1] - school_edges[i][3],
#                             color='orange', alpha=0.2) for i in range(len(sim.schoollist))]
#    proxy.append(plt.Rectangle([0,0], sim.schoollist[0].size[0], sim.schoollist[0].size[1], color='orange', alpha=0.2))
#    for school in schools:
#        ax.add_patch(school)
#    # legend symbol for healthy person
#    proxy.append(Line2D(range(0), range(0), color="bwr"[0], marker='o', alpha=0.8, linewidth=0))
#    # legend symbol for infected person
#    proxy.append(Line2D(range(0), range(0), color="bwr"[2], marker='o', alpha=0.8, linewidth=0))
#    ax.grid(False)
#    ax.spines['top'].set_color('none')
#    ax.spines['bottom'].set_color('none')
#    ax.spines['left'].set_color('none')
#    ax.spines['right'].set_color('none')
#    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
#    ax.legend(proxy, ['House', 'Building', 'Key Building', 'School', 'Healthy', 'Infected'], loc='upper left',
#              bbox_to_anchor=(0, 1), ncol = 4, fontsize=7, edgecolor='w', framealpha=0)
#    return particles, rect
#
#
#def animate(i):
#    """perform animation step"""
#    global sim, rect, ax, fig
#
#    sim.update()
#    rect.set_edgecolor('k')
#    infection_status = np.array(sim.state[1])
#    ax.set_xlim(-120,120)
#    ax.set_ylim(-120,120)
#    text = str(sim.hour) 
#    fig.suptitle('time: '+text+' day: '+str(sim.day),fontsize=10,fontweight=50, x=0.78, y=0.99)
#    positions = [pos+np.random.uniform(low = -2, high=2, size=2) for pos in sim.state[0]]
#    particles.set_offsets(positions)
#    particles.set_array(infection_status)
#    particles.set_alpha(0.8)
#    print(percentage)
#    return particles, rect
#
#ani = animation.FuncAnimation(fig, animate, frames=20000,
#                              interval=100, blit=False, init_func=init)
#
#plt.show()
