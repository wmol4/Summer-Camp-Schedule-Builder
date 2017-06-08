# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:19:31 2017

@author: wluckow
"""

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


all_groups = rows
#location dict: location: (x, y) where x = False --> inside and x = True --> outside. y = the list of groups which can be at that location
location_dict = {"Playground": (True, ["Robins", "Ladybugs", "Lizards", "Mighty Monkeys"]), "Big Gym 1": (False, all_groups), "Big Gym 2": (False, all_groups),
                 "Blacktop": (True, all_groups), "Bunk": (False, all_groups), "Big Field": (True, all_groups), 
                 "Bball Courts": (True, ["Bees", "Dolphins", "Hoppin Roos", "Cool Cats", "Crazy Cats", "Top Dogs"]), "Archery Range": (True, all_groups), 
                 "Ampitheatre": (True, all_groups)}


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
            if val <= 5:
                inout_modified = [column[val]]
            inout_dict[s] = inout_modified

inout_units = list() #all of the different periods and periods +1 (for alternating in and outside)
for key, val in inout_dict.items():
    inout_units.append([key, val[0]])
            
def grid_values(grid): #NOTE: RANDOMIZE WHAT LOCATIONS MUST BE FILLED OUT ALONG THE ROWS
    """
    convert a grid into a dict of {square: char} with a list of all locations for empties
    """
    values = []
    for c in range(len(grid)):
        if grid[c] == '.':
            locations = location_dict.keys()
            print(locations)
            eligible_locations = []
            for loc in locations:
                for groups in location_dict[loc][1]:
                    if groups in boxes[c]:
                        eligible_locations.append(loc)
            values.append(eligible_locations)
        else:
            values.append(boxes[c])
    
    return dict(zip(boxes, values))
    
def column_eliminate(values):
    """
    look through the columns and adjust the values in the 'values' dictionary
    i.e. if the robins period 2 is using big gym half #1, eliminate big gym half #1 from all other groups in period 2
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        location = values[box]
        for col in column_units:
            values[col]
    
    #TODO:
    #implement counters
    #for some locations (i.e. playground and big field, multiple groups can share the space -- create counters for these per column)
    #if the counter runs out, eliminate that location from the rest of the groups

def row_inout_eliminate(values):
    """
    look through adjacent squares and if a value is solved, eliminate all similarly-located locations
    i.e. if robins period 2 is in the big field, then eliminate all outdoor activities from robins period 3
    """
    pass

def row_eliminate(values):
    """
    for certain locations, ensure that a group only goes there once per day
    i.e. if the cool cats use the archery range in period #1, they do not need to visit the archery range again for the rest of the day
    """
    pass

def only_choice(values):
    """
    """
    pass

def naked_twins(values):
    """
    return the values dictionary with naked twins eliminated from their column peers
    """
    pass

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
        values = naked_twins(values)
        
        #only choice
        values = only_choice(values)
        
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
    pass

def solve(grid):
    """
    find the solution
    """
    schedule = grid_values(grid)
    schedule_searched = search(schedule)
    return schedule_searched

solve('..................................................')

#def only_choice(values):
    
    
    
    
