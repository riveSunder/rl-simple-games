import numpy as np
import time
from gym import spaces

class SimEnv():
    def __init__(self, num_vertices=6):

        self.num_vertices = num_vertices
        self.action_dim = self.num_vertices * (self.num_vertices-1)
        self.obs_dim = [self.num_vertices, self.num_vertices]
        self.state = np.zeros((num_vertices,num_vertices,2))
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)

    def check_triangles(self):
        
        # iterate over each vertex
        for ii in range(self.num_vertices):
            print(ii)
            # list vertices connected to vertex ii
            
            connections = [jj if (not(ii==jj) and self.state[ii,jj,0]) else None\
                    for jj in range(self.num_vertices)]
            while None in connections: connections.remove(None)
            if ii == 0:
                #import pdb; pdb.set_trace()
                pass

            # if any two vertices that are connected to vertex ii are connected to each other, \
            # that's a triangle (game over)
            triangles = [self.state[elem,elem2,0] \
                    for elem, elem2 in zip(connections, reversed(connections))]
            print("from vertex {} connections are ".format(ii), connections) 
            
            if np.sum(triangles) > 0:
                print("game over, triangle detected")
            else: 
                print("no triangles detected")

    def disp_state(self):
    
        pass


if __name__ == "__main__":

    env = SimEnv()
    env.check_triangles()
    env.state[0,1,0] = 1
    env.state[1,3,0] = 1
    env.state[0,3,0] = 1
    env.state[1,0,0] = 1
    env.state[3,1,0] = 1
    env.state[3,0,0] = 1
    print(env.state)
    env.check_triangles()


