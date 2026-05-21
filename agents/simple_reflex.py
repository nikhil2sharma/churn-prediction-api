import matplotlib.pyplot  as plt
import matplotlib.patches as mpatches
import time

#Define 2*2 grid environment
enviroment = {
    "Room1":"Clean",
    "Room2":"Dirty", 
    "Room3":"Clean",
    "Room4":"Clean"
}

#Mapping grid to coordinates for visualization
room_coordinates = {
    "Room1": (0, 1),  #Top-left  
    "Room2": (1, 1),  #Top-right
    "Room3": (0, 0),    #Bottom-left
    "Room4": (1, 0)     #Bottom-right
}

rooms= list(enviroment.keys())
agent_index = 0  # Start in Room1

#Reflex agent logic
def simple_reflex_agent(state):
    if state == "Dirty":
        return "Clean" # If the current room is dirty, clean it
    else:
        return "Move"   