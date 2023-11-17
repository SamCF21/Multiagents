from mesa import Agent
import networkx as nx

class Trash(Agent):
    """Trash class for agent"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Charger(Agent):
    """Charger class for agent"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.charging = False 

    def charging(self):
        """Charging function for agent"""
        self.charging = True

class Roomba(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, posCharging):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.posCharging = posCharging
        self.battery = 100
        self.charging = False
        self.graph = nx.grid_2d_graph(model.grid.width, model.grid.height)
        self.visited_positions = set()
   
    def clean_current_cell(self):
        agents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in agents:
            # Remove the trash from the cell
            if isinstance(agent, Trash):
                self.model.grid.remove_agent(agent)
                self.model.schedule.remove(agent)
                self.visited_positions.add(self.pos)

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        next_move = None

        # Mark the current cell as visited
        self.visited_positions.add(self.pos)

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )

        dirty = [position for position in possible_steps if any(isinstance(agent, Trash) for agent in self.model.grid.get_cell_list_contents([position]))]

        if dirty:
            # Choose one dirty cell to move towards (for simplicity, it picks the first one)
            next_move = dirty[0]
        else:
            #Choose from unvisited and truly empty cells
            cells_to_visit = [cell for cell in possible_steps if cell not in self.visited_positions and self.model.grid.is_cell_empty(cell) and not any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents([cell]))]

            if cells_to_visit:
                next_move = self.random.choice(cells_to_visit)
            else:
                #Move randomly to one of the already visited cells in the neighborhood
                visited_cells_in_neighborhood = list(set(possible_steps).intersection(self.visited_positions))
                if visited_cells_in_neighborhood:
                    next_move = self.random.choice(visited_cells_in_neighborhood)

        # Move towards the target cell if next_move is not None
        if next_move is not None:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
            agents = self.model.grid.get_cell_list_contents([next_move])
            for agent in agents:
                if isinstance(agent, Trash):
                    self.clean_current_cell()

    def move_towards_charger(self):
        """
        Move the Roomba towards the charger using Dijkstra's algorithm.
        """
        path = nx.shortest_path(self.graph, source=self.pos, target=self.posCharging)
        if len(path) > 1:
            # The next cell in the path
            next_move = path[1] 
            self.model.grid.move_agent(self, next_move)
            # Adjust battery for the movement
            self.battery -= 1 

    def charge(self):
        # Incremental charging by 5%
        while self.battery < 100:
            self.charging = True
            self.battery = self.battery + 5
            
        if self.battery == 100:
            self.charging = False

    def step(self):
        self.battery -= 1

        if self.battery <= 20:
            self.move_towards_charger()
            # If Roomba reached the charger
            if self.pos == self.posCharging: 
                self.charge()
        else:
            self.move()

        # Check if there are any remaining dirty cells
        dirty = any(isinstance(agent, Trash) for agent in self.model.schedule.agents)
        if not dirty:
            # Stop the simulation
            self.model.running = False 
        

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass




