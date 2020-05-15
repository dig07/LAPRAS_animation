# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 13:16:53 2020

@author: Diganta
"""

'''
Original Person Class:
'''
import numpy as np 
import time
import random
class Person:
  '''Defines a class for the people '''
  def __init__(self,id_number,position, age,vulnerability, infection_status, compliance, commuter, possible_locations, current_location):
    '''Parameters:
    id_number: a string that identifies a person
    position: position of the person [x,y]
    age: age of the person
    vulnerability: coefficient between [0,1]
    infection_status: integer
    compliance: coefficient between [0,1]
    commuter: integer
    possible_locations: list of accessible buildings 
    '''
    self.id_number = id_number
    self.position = position
    self.age = age
    self.vulnerability = vulnerability
    self.infection_status = infection_status # Infection status: 0=Not infected, 1=Infected, asymptomatic, 2=Infected, symptomatic, 3=immune/recovered # not set in stone/decided yet
    self.compliance = compliance
    self.commuter = commuter
    self.possible_locations = possible_locations
    self.current_location = current_location

  def set_schedule(self):
    time = 0
    time_slot_1 = list(self.schedule.keys())[0]
    probs = [(0.25)/(len(self.possible_locations)-2)]*(len(self.possible_locations)-2)
    probs.append(0.75)
    while time < 24:
      if time_slot_1[0]<= time <= time_slot_1[1]:
        time += 1
        pass
      else:
        target = random.choices(self.possible_locations[1:], weights=probs)[0][0]
        if (time_slot_1[0] - time) % 24 > target.duration:
          self.schedule[tuple([time, time+((time_slot_1[0] - time) % 24)])] = self.possible_locations[-1][0]
          time += ((time_slot_1[0] - time) % 24)
        elif (24 - time) > target.duration:
          self.schedule[tuple([time, time+(24-time)])] = self.possible_locations[-1][0]
          time += (24 - time)
        else:
          self.schedule[tuple([time, time+target.duration])] = target
          time += target.duration
        
  def update(self,time,day):
    '''Update '''

    # create dictionary for places to go to in a day
    if time == 0:
      daily_schedule = self.set_schedule()

    # take care of people/infection counters
    for key, value in list(self.schedule.items()):
      if (key[0]<=time<=key[1]):
        self.position = value.position
        if time == key[0]:
          value.people_counter +=1
          value.infected_people += self.infection_status
          self.current_location.people_counter -= 1
          self.current_location.infected_people -= self.infection_status
          self.current_location = value
          # do the infection calc when someone arrives (?)
          if self.infection_status == 0:
            previous_infection_status = self.infection_status
            self.infection_status = self.calculate_infection()
            if self.infection_status != previous_infection_status:
              self.current_location.infected_people += self.infection_status

    # remove all entries bar the first from self.schedule
    if time == 23:
      self.schedule = {list(self.schedule.keys())[0]:list(self.schedule.values())[0]}

    

    # #in_rota = False
    # for key, value in list(self.schedule.items()):
    #   if (key[0]<=time<=key[1]):
    #     self.position = value.position
    #     #in_rota = True
    #     if time == key[0]:
    #       value.people_counter +=1
    #       value.infected_people += self.infection_status
    #       self.current_location.people_counter -= 1
    #       self.current_location.infected_people -= self.infection_status
    #       self.current_location = value
    #       # do the infection calc when someone arrives (?)
    #       if self.infection_status == 0:
    #         previous_infection_status = self.infection_status
    #         self.infection_status = self.calculate_infection()
    #         if self.infection_status != previous_infection_status:
    #           self.current_location.infected_people += self.infection_status

    # if in_rota == False:
    #   probs = [(0.25)/(len(self.possible_locations)-2)]*(len(self.possible_locations)-2)
    #   probs.append(0.75)
    #   target_location = random.choice(random.choice(random.choices(self.possible_locations[1:], weights=probs)))
    #   #print(target_location)
    #   self.position = target_location.position
    #   self.schedule[tuple([time, time+target_location.duration])] = target_location
    #   # added this line to update the person's location (object)
    #   self.current_location = target_location
    
    # if time == 23:
    #   self.schedule = {list(self.schedule.keys())[0]:list(self.schedule.values())[0]}

    # if time >= list(self.schedule.keys())[0][0] and time <= list(self.schedule.keys())[0][1]:
      
      
  def calculate_infection(self):
    infection_calculation = self.vulnerability * (1-self.compliance) * self.current_location.calculate_infectivity()
    return random.choices([0,1], weights=[1-infection_calculation, infection_calculation])[0]

class Child(Person):
  '''A subclass of Person that defines a child'''
    
  def __init__(self,id_number,position, age, vulnerability, infection_status, compliance, commuter, possible_locations,current_location):
    '''Parameters:
    id_number: a string that identifies a person
    position: position of the person [x,y]
    age: age of the person
    vulnerability: coefficient between [0,1]
    infection_status: 
    compliance: coefficient between [0,1]
    commuter: integer
    possible_locations: list of accessible buildings 
    '''
    super().__init__(id_number+'_Child',position, age, vulnerability, infection_status, compliance, commuter, possible_locations,current_location)
    # where children go at given times
    self.school = np.random.choice(possible_locations[0])
    self.schedule = {tuple([8,15]):self.school}
        

class Worker(Person):
  '''A subclass of Person that defines a (regular) worker'''
  def __init__(self,id_number,position, age, vulnerability, infection_status, compliance, commuter, possible_locations,current_location):
    '''Parameters:
    id_number: a string that identifies a person
    position: position of the person [x,y]
    age: age of the person
    vulnerability: coefficient between [0,1]
    infection_status: 
    compliance: coefficient between [0,1]
    commuter: integer
    possible_locations: list of accessible buildings
    '''
    super().__init__(id_number+'_Worker',position, age, vulnerability, infection_status, compliance, commuter, possible_locations,current_location)
    # where workers go at given times
    self.building = np.random.choice(possible_locations[0])
    self.schedule = {tuple([9,17]):self.building}
        
class Key_Worker(Person):
  '''A subclass of Person that defines a key worker'''
  def __init__(self,id_number,position, age, vulnerability, infection_status, compliance, commuter, possible_locations,current_location):
    '''Parameters:
    id_number: a string that identifies a person
    position: position of the person [x,y]
    age: age of the person
    vulnerability: coefficient between [0,1]
    infection_status: 
    compliance: coefficient between [0,1]
    commuter: integer
    possible_locations: list of accessible buildings
    '''
    super().__init__(id_number+'_Keyworker',position, age, vulnerability, infection_status, compliance, commuter, possible_locations, current_location)
    offset = np.random.randint(-9,7)
    # where key workers go at given times (w/ random offset)
    self.key_building = np.random.choice(possible_locations[0])
    self.schedule = {tuple([9+offset,17+offset]):self.key_building}
