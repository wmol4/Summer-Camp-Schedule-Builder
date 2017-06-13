# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:19:31 2017

@author: wluckow
"""
import pandas as pd


df = pd.read_csv(<URL HERE>, index_col = 0, header = 0)
df = df.fillna('.') #fill in blanks with a period

data = []

for tuples in df.itertuples(index = False):
    for value in tuples:
        data.append(value)
        
print(data)


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

rows = ["Robins",
        "Ladybugs",
        "Bees",
        "Dolphins",
        "Lizards",
        "Mighty Monkeys",
        "Hoppin Roos",
        "Cool Cats",
        "Crazy Cats",
        "Top Dogs"]
columns = ["Period 1",
           "Period 2",
           "Period 3",
           "Period 4",
           "Period 5",
           "Period 6"]
boxes = cross_list(rows, columns)

#activities = ["$10 Ball", "Archery", "Arts & Crafts", "Basketball", "Bunk Time", "Camouflage", "Camp Games", "Capture the Flag", "Chaos Ball", "Dance", "Drama", "Football",
#              "Freeze Dance", "Game Time", "Gladiator", "Group Time", "Handball", "Hockey", "Human Bowling", "Karaoke", "Kickball", "Lanyards", "Music", "Parachute", "Playground",
#              "RMDC Ball", "Tag Games", "Scooters", "Storm the Castle", "Volleyball", "War o Worlds"]         
#weekly_activity = np.zeros((len(rows), len(activities)))

#group_activity = {"Robins": ["Chaos Ball", "Camouflage", "Bunk Time", "Arts & Crafts", "Archery", "Scooters", "Dance", "Game Time", "Human Bowling", "Karaoke", "Lanyards", "Music", "Parachute", "Playground", "Tag Games"]}

all_groups = rows
young_2_groups = ["Robins", "Ladybugs", "Lizards", "Mighty Monkeys"]
young_3_groups = ["Robins", "Ladybugs", "Bees", "Lizards", "Mighty Monkeys", "Roos"]
old_groups = ["Dolphins", "Crazy Cats", "Top Dogs"]
more_old_groups = ["Bees", "Dolphins", "Hoppin Roos", "Cool Cats", "Crazy Cats", "Top Dogs"]

#location dict: location: (a, b, c, d, e) where 
    #a = True --> outside;;;; false --> inside
    #b = True --> active location ;;;;; false --> passive location
    #c = the list of groups which can be at that location. 
    #d = the number of groups that can be at that location at any given time 
    #e = number of times a group can go to that location in a single day

location_dict = {"Big Gym": (False, True, all_groups, 2, 3),
                 "Blacktop/Playground": (True, True, all_groups, 3, 2),
                 "Big Field": (True, True, all_groups, 4, 2),
                 "Water World": (True, False, all_groups, 6, 1),
                 "Archery Range": (True, False, all_groups, 1, 1),
                 "Cafeteria": (False, False, young_2_groups, 1, 1),
                 "Arts and Crafts": (False, False, young_3_groups, 1, 1),
                 "Ampitheater": (False, False, all_groups, 1, 1),
                 "Game Room": (False, False, all_groups, 1, 1),
                 'Bunk': (False, True, young_2_groups, len(rows), 1)}
                 
#go through data and if there is some location which is not in the location dict, ask the user
#if the location is inside or outside
for i in range(len(data)):
    if data[i] != '.' and data[i] not in location_dict.keys():
        inside_outside = input("Is {} an OUTDOOR location? \n Type 'y' or 'yes' if the location is OUTSIDE \n Type 'n' or 'no' if the location is an INDOOR location: ".format(data[i]))
        if inside_outside.lower() == 'y' or inside_outside.lower() == 'yes':
            print("{} is outside.".format(data[i]))
            inside_outside = True
        else:
            print("{} is inside.".format(data[i]))
            inside_outside = False
        temp_group = rows[i//len(columns)]
        print("Only {} will go to {}.".format(temp_group, data[i]))
        print("")
        location_dict[data[i]] = (inside_outside, False, [temp_group], 1, 1)
            

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
            if str(6) not in s and str(2) not in s:
                inout_dict[s] = inout_modified

inout_units = list() #all of the different periods and periods +1 (for alternating in and outside)
for key, val in inout_dict.items():
    inout_units.append([key, val[0]])
    
#[location, frequency]
period_loc_frequency = dict()
for loc in location_dict.keys():
    period_loc_frequency[loc] = location_dict[loc][3]
    
group_loc_frequency = dict()
for loc in location_dict.keys():
    group_loc_frequency[loc] = location_dict[loc][4]
            
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
                for groups in location_dict[loc][2]:
                    if groups in boxes[c]:
                        eligible_locations.append(loc)
            values.append(eligible_locations)
        else:
            values.append([grid[c]])
            
    values = dict(zip(boxes, values))
    
    return values
    
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
        
        if location in location_dict.keys():
            outside = location_dict[location][0]
 
            if str(6) not in box and str(2) not in box: #only look at periods 1-5
            
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
    
def row_active_eliminate(values):
    """
    look through rows and ensure that each group gets at least 3 active locations
    active locations = gym, big field, blacktop, playground.
    """
    
    #count up how many active locations there are so far in each row = x
    #if x + the number of non-solved spots = 3:
        #eliminate non-active values from all non-solved spots
    
    return values

def row_eliminate(values):
    """
    for certain locations, ensure that a group only goes there a certain number of times (location_dict[4]) per day
    i.e. if the cool cats use the archery range in period #1, they do not need to visit the archery range again for the rest of the day
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
            
        location = values[box][0]
        
        if location in location_dict.keys():

            for other_row in row_dict[box]:
                try:
                    values[other_row].remove(location)
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
        values = row_active_eliminate(values)
        values = row_eliminate(values)
        
        
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
                #print("Successfully assigned {} to {}".format(value, s))
                return attempt
        except:
            #print("Failed assigning {} to {}".format(value, s))
            pass

def solve(grid):
    """
    find the solution
    """
    schedule = grid_values(grid)
    schedule_searched = search(schedule)
    return schedule_searched

schedule = solve(data)
for i in boxes:
    print(i, "|||", schedule[i])


    
    
    
    
