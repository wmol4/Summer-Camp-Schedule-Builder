# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:19:31 2017

@author: wluckow
"""
import numpy as np


def cross_list(A, B):
    "Cross product of elements in A and elements in B."
    boxes = []
    for s in A:
        for t in B:
            boxes.append(s+t)
    return boxes
    
def cross_rows(A, B):
    boxes = []
    for t in B:
        boxes.append(A+t)
    return boxes
    
def cross_columns(A, B):
    boxes = []
    for s in A:
        boxes.append(s+B)
    return boxes

rows = ["Robins", "Ladybugs", "Bees", "Dolphins", "Lizards", "Mighty Monkeys", "Hoppin Roos", "Cool Cats", "Crazy Cats", "Top Dogs"]
columns = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6"]
boxes = cross_list(rows, columns)

activities = ["4-Way CTF", "$10 Ball", "Archery", "Arts & Crafts", "Basketball", "Bunk Time", "Camouflage", "Camp Games", "Capture the Flag", "Chaos Ball", "Dance", "Drama", "Football",
              "Freeze Dance", "Game Time", "Gladiator", "Group Time", "Handball", "Hockey", "Human Bowling", "Karaoke", "Kickball", "Lanyards", "Music", "Parachute", "Playground",
              "RMDC Ball", "Tag Games", "Scooters", "Storm the Castle", "Volleyball", "War o Worlds"]
              
weekly_activity = np.zeros((len(rows), len(activities)))

#group_activity = {"Robins": ["Chaos Ball", "Camouflage", "Bunk Time", "Arts & Crafts", "Archery", "Scooters", "Dance", "Game Time", "Human Bowling", "Karaoke", "Lanyards", "Music", "Parachute", "Playground", "Tag Games"]}

all_groups = rows
#location dict: location: (x, y, z) where x = False --> inside and x = True --> outside. y = the list of groups which can be at that location. z = the number of groups that can be at that location at any given time
location_dict = {"Playground": (True, ["Robins", "Ladybugs", "Lizards", "Mighty Monkeys"], 2), "Big Gym 1": (False, all_groups, 1), "Big Gym 2": (False, all_groups, 1),
                 "Blacktop": (True, all_groups, 1), "Bunk": (False, all_groups, len(rows)), "Big Field": (True, all_groups, 4), 
                 "Bball Courts": (True, ["Bees", "Dolphins", "Hoppin Roos", "Cool Cats", "Crazy Cats", "Top Dogs"], 1), "Archery Range": (True, all_groups, 1), 
                 "Ampitheatre": (False, all_groups, 1), "Game Room": (False, all_groups, 1), "Cafeteria": (False, all_groups, 1)}


row_units = [cross_rows(r, columns) for r in rows] #all of the different rows
row_dict = dict()
for s in boxes: #iterate over every possible grid space
    for row in row_units: #iterate over thw rows
        if s in row:
            row_modified = list(row)
            row_modified.remove(s)
            row_dict[s] = row_modified
            
column_units = [cross_columns(rows, c) for c in columns] #all of the different columns
column_dict = dict()
for s in boxes:
    for column in column_units:
        if s in column:
            column_modified = list(column)
            column_modified.remove(s)
            column_dict[s] = column_modified
            
inout_units = row_units
inout_dict = dict()
for s in cross_list(rows, columns[:len(columns)-1]):
    for column in inout_units:
        if s in column:
            val = int(s[len(s) - 1:len(s)])
            inout_modified = [column[val]]
            if str(3) not in s and str(6) not in s:
                inout_dict[s] = inout_modified

inout_units = list() #all of the different periods and periods +1 (for alternating in and outside)
for key, val in inout_dict.items():
    inout_units.append([key, val[0]])
    
#[location, frequency]
period_loc_frequency = dict()
for loc in location_dict.keys():
    period_loc_frequency[loc] = location_dict[loc][2]
            
def grid_values(grid):
    """
    convert a grid into a dict of {square: char} with a list of all locations for empties
    """
    values = []
    for c in range(len(grid)):
        if grid[c] == '.':
            locations = location_dict.keys()
            eligible_locations = []
            for loc in locations:
                for groups in location_dict[loc][1]:
                    if groups in boxes[c]:
                        eligible_locations.append(loc)
            values.append(eligible_locations)
        else:
            values.append([grid[c]])
    return dict(zip(boxes, values))
    
def column_eliminate(values):
    """
    look through the columns and adjust the values in the 'values' dictionary
    i.e. if the robins period 2 is using big gym half #1, eliminate big gym half #1 from all other groups in period 2
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        
        location = values[box][0] #a solved location in a column
        if location in location_dict.keys():
            
            #ensure that multiple groups can be in multiple locations using period_loc_frequency
            loc_freq = 0
            loc_freq -= 1 #subtract one for the current location usage
            loc_freq += period_loc_frequency[location]
            
            for other_col in column_dict[box]:
                if other_col in solved_values:
                    if values[other_col] == location:
                        loc_freq -= 1
            
            #make sure that too many locations haven't been used up yet
            if loc_freq < 0:
                print("error: too many groups in location", location)
            
            #if the location is "used up", remove it as an option from the rest of the groups
            if loc_freq == 0:
                for other_col in column_dict[box]:
                    try:
                        values[other_col].remove(location) #remove the location from the other column units
                    except:
                        pass
                
    return values

def row_inout_eliminate(values):
    """
    look through adjacent squares and if a value is solved, eliminate all similarly-located locations
    i.e. if robins period 2 is in the big field, then eliminate all outdoor activities from robins period 3
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        location = values[box][0]
        outside = location_dict[location][0]
     
        if str(6) not in box and str(3) not in box: #only look at periods 1-5
        
            following_activity = inout_dict[box][0]
            if following_activity not in solved_values:
                temp_list = list(values[following_activity])
                
                for locations_next in values[following_activity]:
                    
                    if location_dict[locations_next][0] == outside and outside == True:
                        
                        try:
                            temp_list.remove(locations_next)
                        except:
                            pass

                
                values[following_activity] = temp_list


    return values

def row_eliminate(values):
    """
    for certain locations, ensure that a group only goes there once per day
    i.e. if the cool cats use the archery range in period #1, they do not need to visit the archery range again for the rest of the day
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        
        location = values[box][0]
        
        for other_row in row_dict[box]:
            try:
                values[other_row].remove(location)
            except:
                pass

            
    return values

def row_naked_twins(values):
    """
    if 2 entries in a column both share the same two possibilities, remove those possibilities from all other entries in that column
    """
    dual_values = [box for box in values.keys() if len(values[box]) == 2]
    
    for box in dual_values:
        for row_boxes in row_dict[box]:
            if values[row_boxes] == values[box]:
                loc_1 = values[box][0]
                loc_2 = values[box][1]
        
        modified_row = list(row_dict[box])
        modified_row.remove(row_boxes) #we do not want to remove the values from naked twins
        
        for modified in modified_row: #for all the OTHER columns:
            if len(values[modified]) == 1: #we do not want to remove values from solved entries
                modified_row.remove(modified)
                         
        for row_boxes_2 in modified_row:
            try:
                values[row_boxes_2].remove(loc_1)
            except:
                pass
            try:
                values[row_boxes_2].remove(loc_2)
            except:
                pass
            

    
    return values

def reduce_schedule(values):
    stalled = False
    while not stalled:
        #how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        #eliminate
        values = column_eliminate(values)
        values = row_inout_eliminate(values)
        values = row_eliminate(values)
        
        #naked twins strategy
        #values = row_naked_twins(values)
        
        #check how many boxes now have a determined value
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        #if no new values were added, stop the loop
        stalled = solved_values_before == solved_values_after
        
        #return false if there is some box which has no possible values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values

def search(values):
    """
    if reducing the schedule stalled out, randomly (weighted) assign a group to a location
    """
    
    values = reduce_schedule(values)
    
    if values is False:
        return False ## failed earlier
    
    if all(len(values[s]) == 1 for s in boxes):
        return values ## solved!
        
    #choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)    
    
    #using reccurence, solve each one of the resulting schedules
    for value in values[s]:
        try:
            new_schedule = values.copy()
            new_schedule[s] = [value]
            attempt = search(new_schedule)
            if attempt:
                print("Successfully assigned {} to {}".format(value, s))
                return attempt
        except:
            print("Failed assigning {} to {}".format(value, s))
    

def solve(grid):
    """
    find the solution
    """
    schedule = grid_values(grid)
    schedule_searched = search(schedule)
    return schedule_searched

schedule = solve(['.', '.', '.', 'Water World', '.', '.', '.', '.', '.', 'Water World', '.', '.','.', '.', '.', 'Water World', '.', '.','.', '.', '.', 'Water World', '.', '.','.', '.', '.', '.', 'Water World', '.','.', '.', '.', '.', 'Water World', '.','.', '.', '.', '.', 'Water World', '.','.', '.', '.', '.', 'Water World', '.','.', '.', '.', '.', 'Water World', '.','.', '.', '.', '.', 'Water World', '.'])
print(schedule)

#def only_choice(values):
    
    
    
    
