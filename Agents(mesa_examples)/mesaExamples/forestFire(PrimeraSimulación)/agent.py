from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Alive", "Dead"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Alive"
        self._next_condition = None

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        """"""
        if self.condition == "Dead" and self.pos[1] < 49 and self.pos[0] > 0 and self.pos[0] < 49: 
            upperneigbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                #saves the neighbors in a list vewing their postition as a tuple
                if neighbor.pos[1] == self.pos[1] + 1:
                    upperneigbors.append(neighbor)
                #chechks upperneigbors[0] and upperneigbors[2] to see if they are alive and if they are it sets the next condition to alive
            if ((upperneigbors[0].condition == "Dead") and (upperneigbors[2].condition == "Alive")):
                self._next_condition = "Alive"
                
            if((upperneigbors[2].condition == "Dead") and (upperneigbors[0].condition == "Alive")):
                self._next_condition = "Alive"

    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition