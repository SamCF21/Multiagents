#Samantha Covarrubias - A01026174

from model import RandomModel, Trash, Roomba, ObstacleAgent, Charger
from mesa.visualization import CanvasGrid, ChartModule
from mesa.visualization import ModularServer
from mesa.datacollection import DataCollector

def agent_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0, "r": 0.5}
    
    if isinstance(agent, Roomba):
        portrayal["Color"] = "#000000"
        portrayal["Layer"] = 2
        
    elif isinstance(agent, Trash):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    elif isinstance(agent, Charger):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
    elif isinstance(agent, ObstacleAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 3
    
    return portrayal

def compute_percent_clean(model):
    num_clean_cells = sum(1 for cell in model.grid.get_all_cell_contents() if isinstance(cell, Trash))
    total_cells = model.grid.width * model.grid.height
    return (num_clean_cells / total_cells) * 100 if total_cells > 0 else 0

model_params = {"N": 5, "width": 10, "height": 10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# DataCollector for tracking simulation data
data_collector = DataCollector(
    agent_reporters={"Steps Taken": "steps_taken"},  # Number of movements performed by the agent
)

# ChartModules for visualizing the data
chart1 = ChartModule([{"Label": "Steps Taken", "Color": "#000000"}], data_collector_name="datacollector")
chart2 = ChartModule([{"Label": "Percentage of Clean Cells", "Color": "green", "AgentReporters": "compute_percent_clean"}], data_collector_name="datacollector")

server = ModularServer(RandomModel, [grid, chart1, chart2], "Roomba", model_params)

server.port = 8521  # The default
server.launch()
