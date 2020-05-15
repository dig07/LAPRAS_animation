# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:36:28 2020
"""
from Person import Person, Worker, Child, Key_Worker
import numpy as np 
import time
import random
class Environment:

    def __init__(self, name, position, size, people_counter, infected_people, duration, capacity):
        '''Size  - tuple (x,y)'''
        self.position = position
        self.name = name
        self.size = size
        self.people_counter = people_counter
        self.infected_people = 0
        self.duration = duration
        self.capacity = capacity

    def calculate_infectivity(self):
      '''n.b. change sizes, also factor of 10 is random'''
      return 10*4*self.infected_people / (self.people_counter * self.size[0] * self.size[1])

class Transport(Environment):
	
    def __init__(self, name, position, size, people_counter, infected_people, duration, capacity, velocity):
        self.velocity = velocity

        super().__init__(name, position, size, people_counter, infected_people, duration, capacity)

class House(Environment):
  '''Defines a class for the houses of the population: houses are instantiated with a given number of people (between 1 and 5, with at least one regular worker).''' 
  def __init__(self, name, position, size, people_counter, infected_people, duration, capacity,buildinglist,key_building_list,schoollist):
    '''Parameters:
    name: name of the building
    position: position on the map
    size: size of building on board
    people_counter: number of people in house, integer
    infected_people: number of infected people in house, integer
    duration: turns for which person stays in house
    capacity: max number of people in house
    buildinglist: buildings where workers can work
    key_building_list: key buildings where key workers work
    schoollist: list of schools where are children'''
    super().__init__(name, position, size, people_counter, infected_people, duration, capacity)
    if infected_people > 0:
      infection_status = 1
    else: infection_status = 0
    # ensure there is always at least one adult/regular worker in a household
    self.house_personlist = [Worker(name+'_'+str(0),position,np.random.randint(20,80),1,infection_status,0,1,[key_building_list,buildinglist,schoollist,[self]],self)]
    # random ages for the remaining people in house
    agelist = np.random.randint(0,80,people_counter-1)
    for index, age in enumerate(agelist):
      if age <= 20: # children
        self.house_personlist.append(Child(name+'_'+str(index+1), position, age, 1, infection_status, 0, 1,[schoollist,buildinglist,[self]],self))
      else: # adults
        if np.random.rand() > 1/2: # key workers
          self.house_personlist.append(Key_Worker(name+'_'+str(index+1), position, age, 1, infection_status, 0, 1,
          [key_building_list,buildinglist,schoollist,[self]],self))
        else: # normal workers
          self.house_personlist.append(Worker(name+'_'+str(index+1),position,age,1,infection_status,0,1, [buildinglist,key_building_list,buildinglist,[self]],self))

  def calculate_infectivity(self):
      '''n.b. change sizes'''
      if self.infected_people > 0: return 1
      else: return 0
      
