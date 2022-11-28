import random
import statistics
import numpy as np
from numpy import genfromtxt
import pandas as pd
import json 
import numpy

from classes import *


contnr_size = 240
max_daily_orders = 120
daily_items_avg = 18000
daily_items_std = 8000

order_size_min = 10
order_size_max = 240

num_operators=10
num_emptying_operators=2

scan_containor_time_avg=10
scan_containor_time_std=2

item_scan_time_avg=3
item_scan_time_std=1.5

cont_right_itm_avg = 150
cont_right_itm_std = 70

emptying_chutes_avg=2
emptying_chutes_std=1

num_operators=10

# -----------------------
# total daily items:
total_items = int(random.gauss(daily_items_avg, daily_items_std))

# list of objects
orders = []
containors = []
operators = []
time=0
# -----------------------
# Create order objects:

remaining_daily_items = total_items
while (remaining_daily_items > 0) & (len(orders) < max_daily_orders):
    _size = numpy.random.randint(order_size_min, order_size_max + 1)
    _size = min(_size, remaining_daily_items)
    orders.append(order(_size))
    remaining_daily_items = remaining_daily_items - _size

i=0
while (remaining_daily_items > 0)& (i < max_daily_orders):
    _size = numpy.random.randint(0, order_size_max - orders[i].size+ 1)
    _size = min(_size, remaining_daily_items)
    new_size = orders[i].size + _size

    orders[i].size = new_size
    remaining_daily_items = remaining_daily_items - _size
    i=i+1

# -----------------------
# Create containor objects:
remaining_items = total_items
i=0
while remaining_items > 0:
    num_right_itm_in_contnr = int(random.gauss(cont_right_itm_avg, cont_right_itm_std))
    num_right_itm_in_contnr = min(num_right_itm_in_contnr, contnr_size)
    num_right_itm_in_contnr = min(num_right_itm_in_contnr, remaining_items)

    # Exluding containors with zero right items:
    if (num_right_itm_in_contnr > 0): 
        containors.append(containor(num_right_itm_in_contnr,i))
        remaining_items = remaining_items - num_right_itm_in_contnr
        i=i+1

# -----------------------
# Create operator objects:
for i in range(num_operators):
    operators.append(operator(i))

#-----------------------------


def assign_itm_chute(): 
     
    chute_id=numpy.random.randint(0, len(orders))
    if orders[chute_id].filled < orders[chute_id].size :
        orders[chute_id].filled = orders[chute_id].filled + 1
        orders[chute_id].filled_t.append(TIME)
        return chute_id

    # check chute ids greater than the random generated one
    chute_id_init=chute_id
    flag = orders[chute_id].filled > orders[chute_id].size
    while (flag) & (chute_id<len(orders)):
        chute_id+=1
        flag = orders[chute_id].filled > orders[chute_id].size
    
    if orders[chute_id].filled < orders[chute_id].size :
        orders[chute_id].filled = orders[chute_id].filled + 1
        orders[chute_id].filled_t.append(TIME)
        return chute_id
    
    # check chute ids less than the random generated one
    chute_id=chute_id_init
    while flag:
        chute_id-=1
        flag = orders[chute_id].filled > orders[chute_id].size

    if orders[chute_id].filled < orders[chute_id].size :
        orders[chute_id].filled = orders[chute_id].filled + 1
        orders[chute_id].filled_t.append(TIME)

        return chute_id


events = LinkedList()

# START SIMULATION
# assign first containors
for i in range (num_operators):
    operators[i].containor = containors[i].id
    operators[i].remaining_items_in_containor = containors[i].right_items
    operators[i].next_available_time = 0

    containors[i].start_time = 0
    containors[i].operator = operators[i].id

    events.insert(0,operators[i].id, containors[i].id ,  'containor_arrived')
last_arrived_containor_id = num_operators-1

# RUN SIMULATION
# run while there is an event:
while events.head != None:

    ID   = events.head.operator_id
    C_ID = events.head.containor_id
    TYPE = events.head.type
    TIME = events.head.time
    events.delete()

    if TYPE == 'containor_arrived' :
        # update the operator object:
        next_time = TIME + random.gauss(scan_containor_time_avg, scan_containor_time_std)

        operators[ID].containor = C_ID
        operators[ID].next_available_time = next_time
        operators[ID].remaining_items_in_containor = containors[C_ID].right_items

        containors[C_ID].operator = ID
        containors[C_ID].start_time = TIME

        events.insert(next_time, ID, C_ID, 'item_scanned')

    if TYPE == 'item_scanned' :
        operators[ID].remaining_items_in_containor = operators[ID].remaining_items_in_containor -1
        
        # assign an item to chutes:
        assign_itm_chute()
        
        if operators[ID].remaining_items_in_containor > 0 :
            next_time = TIME + random.gauss(item_scan_time_avg, item_scan_time_std)
            operators[ID].next_available_time = next_time

            events.insert(next_time, ID, C_ID, 'item_scanned')
        
        else:
            #finished current containor
            containors[C_ID].end_time = TIME
            
            #new containor will arrive:
            last_arrived_containor_id+=1
            if (last_arrived_containor_id<len(containors)):
                C_ID_new=last_arrived_containor_id
                events.insert(TIME, ID, C_ID_new, 'containor_arrived')
    
# now let's check orders and their filled time:


def find_min():
    _min=orders[0].filled_t[-1]
    min_id=0
    for i in range (len(orders)): 
        if ( (_min > orders[i].filled_t[-1]) & (orders[i].emptying_processed == -1 ) ):
            _min=orders[i].filled_t[-1]
            min_id=i
    if orders[min_id].emptying_processed == -1 :
        return _min,min_id

# -----------------------
# Create emptying operator objects:
empt_operators = []

for i in range(2):
    empt_operators.append(emptying_operator(i)) 

#------------
# emptying_events:
def simulate_v2():
    e_events = LinkedList()

    #simulate emptying the chutes:
    for i in range (2):
        _min,min_id=find_min()

        orders[min_id].emptying_processed = 1
        current_t=_min
        for j in range(orders[min_id].size):
            current_t = current_t + random.gauss(emptying_chutes_avg, emptying_chutes_std)

        orders[min_id].emptying_end_t = current_t
        
        empt_operators[i].order=min_id
        empt_operators[i].next_available_time = current_t

        e_events.insert(current_t,empt_operators[i].id, min_id,  'finished_emptying')

    #while e_events.head != None:
    for x in range(len(orders)-num_emptying_operators):
        ID   = e_events.head.operator_id
        C_ID = e_events.head.containor_id
        TYPE = e_events.head.type
        TIME = e_events.head.time
        e_events.delete()

        if (find_min()):
            _min,min_id=find_min()
            orders[min_id].emptying_processed = 1

            if (_min > TIME):
                current_t=_min
            else:
                current_t=TIME

            for j in range(orders[min_id].size):
                current_t = current_t + random.gauss(emptying_chutes_avg, emptying_chutes_std)
            orders[min_id].emptying_end_t = current_t

            empt_operators[ID].order=min_id
            empt_operators[ID].next_available_time = current_t

            e_events.insert(current_t,empt_operators[ID].id, min_id,  'finished_emptying')


# 2 employees:
def find_max_time():
    _maxt=empt_operators[0].next_available_time
    for i in range (len(empt_operators)): 
        if _maxt<empt_operators[i].next_available_time:
            _maxt=empt_operators[i].next_available_time
    return _maxt

# reset variables:
def reset_vars():
    for i in range(len(orders)):
        orders[i].emptying_start_t = -1
        orders[i].emptying_end_t = -1
        orders[i].emptying_processed = -1
    for j in range(len(empt_operators)):
        empt_operators[j].next_available_time=-1
        empt_operators[j].order=-1

results=[]
for num_employees in range(2,11):
    reset_vars()
    num_emptying_operators=num_employees
    simulate_v2()

    results.append(find_max_time())


#plot
import matplotlib.pyplot as plt

# Make a random dataset:
height = results
bars = ('2', '3', '4', '5', '6','7','8','9','10')
y_pos = np.arange(len(bars))

# Create bars
plt.bar(y_pos, height)

# Create names on the x-axis
plt.xticks(y_pos, bars)
plt.xlabel('Number of Operators')
plt.ylabel('Total Time')
plt.title('Total Time vs Number of Operators')
# Show graphic
plt.show()