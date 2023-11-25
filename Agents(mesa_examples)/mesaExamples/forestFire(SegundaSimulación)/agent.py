from mesa import Agent


class TreeCell(Agent):
    """
        A tree cell.

        Attributes:
            x, y: Grid coordinates
            condition: Can be "Alive" or "Dead"
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
        if self.condition == "Dead":
            all_neighbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if self.pos[1] == 49:
                    if neighbor.pos[1] == 0:
                        all_neighbors.append(neighbor)
                else:
                    if self.pos[1] + 1 == neighbor.pos[1]:
                        all_neighbors.append(neighbor)

            #chechks all_neighbors[0] and all_neighbors[2] to see if they are alive and if they are it sets the next condition to alive
            if ((all_neighbors[0].condition == "Dead") and (all_neighbors[2].condition == "Alive")):
                self._next_condition = "Alive"
                
            if((all_neighbors[2].condition == "Dead") and (all_neighbors[0].condition == "Alive")):
                self._next_condition = "Alive"

        if self.condition == "Alive":
            all_neighbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if self.pos[1] == 49:
                    if neighbor.pos[1] == 0:
                        all_neighbors.append(neighbor)
                else:
                    if self.pos[1] + 1 == neighbor.pos[1]:
                        all_neighbors.append(neighbor)
            #checks if the neighbors are alive or dead and sets the next condition to dead
            if ((all_neighbors[0].condition == "Dead" and all_neighbors[1].condition == "Dead" and all_neighbors[2].condition == "Dead") or

                (all_neighbors[0].condition == "Dead" and all_neighbors[1].condition == "Alive" and all_neighbors[2].condition == "Dead") or

                (all_neighbors[0].condition == "Alive" and all_neighbors[1].condition == "Dead" and all_neighbors[2].condition == "Alive") or

                (all_neighbors[0].condition == "Alive" and all_neighbors[1].condition == "Alive" and all_neighbors[2].condition == "Alive")):
                self._next_condition = "Dead"

    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
