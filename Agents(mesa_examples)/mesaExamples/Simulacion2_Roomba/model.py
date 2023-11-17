from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import Roomba, Trash, Charger, ObstacleAgent

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height):
        self.current_id = 0
        self.num_agents = N

        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, Roomba) else 0})

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        
        #Random pos
        randompos = lambda w,h: (self.random.randrange(w), self.random.randrange(h))

       #Creates obstacles
        for pos in border:
            obs= ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
        
        #Create charger
        for i in range(3):
            chargerpos = randompos(self.grid.width, self.grid.height)
            charger = Charger(self.next_id(), self)
            roomba = Roomba(self.next_id(), self, chargerpos)
            self.schedule.add(charger)
            self.schedule.add(roomba)
            chargerpos = randompos(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(chargerpos)):
                chargerpos = randompos(self.grid.width, self.grid.height)
            self.grid.place_agent(charger, chargerpos)
            self.grid.place_agent(roomba, chargerpos)

        #Create obstacles
        for i in range(10):
            obs = ObstacleAgent(self.next_id(), self)
            self.schedule.add(obs)
            pos = randompos(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = randompos(self.grid.width, self.grid.height)
            self.grid.place_agent(obs, pos)

        #Create trash
        for i in range(15):
            trash = Trash(self.next_id(), self)
            self.schedule.add(trash)
            pos = randompos(self.grid.width, self.grid.height)
            while not self.grid.is_cell_empty(pos):
                pos = randompos(self.grid.width, self.grid.height)
            self.grid.place_agent(trash, pos)
            
    def next_id(self):
            self.current_id += 1
            return self.current_id

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
