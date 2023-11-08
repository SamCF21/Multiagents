import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation

from agent import TreeCell

class ForestFire(Model):
    def _init_(self, height=50, width=50, density=0.65):
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=False)
        
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead"),
            }
        )

        for contents, (x, y) in self.grid.coord_iter():
            new_tree = TreeCell((x, y), self, density)
            if self.random.random() < density:
                new_tree.condition = "Alive"
            self.grid.place_agent(new_tree, (x, y))
            self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
    @staticmethod
    def count_type(model, tree_condition):
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count