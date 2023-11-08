from mesa import Agent
import random

statusDictionary = {("Dead", "Dead", "Dead"):"Dead",
                        ("Dead","Dead","Alive"):"Alive",
                        ("Dead","Alive","Dead"):"Dead",
                        ("Dead","Alive","Alive"):"Alive",
                        ("Alive","Dead","Dead"):"Alive",
                        ("Alive","Dead","Alive"):"Dead",
                        ("Alive","Alive","Dead"):"Alive",
                        ("Alive","Alive","Alive"):"Dead"
                        }

class TreeCell(Agent):
    
    def _init_(self, pos, model, density):
        super()._init_(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None
        self.density = density

    def step(self):
        neighborStates = []
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            if neighbor.pos[1] > self.pos[1]:
                neighborStates.append(neighbor.condition)
        if self.pos[1] != 49:
            self._next_condition = statusDictionary.get(tuple(neighborStates))
        else:
            if random.random() < self.density:
                self.condition = "Alive"
            else:
                self.condition = "Dead"
        
    def advance(self):
        if self._next_condition is not None:
            self.condition = self._next_condition