import numpy as np
import time
from gym import spaces

class SimpleGameEnv():
    def __init__(self):
        num_vertices = 1
        self.state = np.zeros((num_vertices,num_vertices))
        self.reset()
    def step(self,action,player):
        pass
    def reset(self):
        pass
    def check_game_over(self):
        pass
    def disp_game(self):
        print(self.state)

class SimEnv(SimpleGameEnv):
    def __init__(self, num_vertices=6):

        self.num_vertices = num_vertices
        self.action_dim = 15 #self.num_vertices * (self.num_vertices-1)
        self.obs_dim = [self.action_dim, 2]
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)
        self.act_dict = []
        [[self.act_dict.append([jj,ii]) \
                for ii in range(jj+1,self.num_vertices)] \
                for jj in range(self.num_vertices)]

    def reset(self):
        self.state = np.zeros((self.num_vertices,self.num_vertices,2))
        self.legal_moves = [ii for ii in range(self.action_dim)]
        self.obs = np.zeros((self.action_dim, 2))
        obs = self.obs

        return obs

    def step(self, action, player=0):

        try:
            _ = self.obs
        except:
            print("call env.reset before env.step")
            self.reset()

        assert len(self.legal_moves) is not 0, print("game is over, please reset")

        edge = self.act_dict[action]

        if action in self.legal_moves:
            self.state[edge[0], edge[1], player] = 1.0
            self.legal_moves.remove(action)
            self.obs[action,player] = 1.0 
        else:
            # illegel move, edge alre
            illegal = True
            done = True
            print("illegal move attempted by player ", player)

        triangles = self.check_game_over(player)

        if triangles:
            done = True
            reward = -1.0

        reward = 1.0 if (not done and len(self.legal_moves==1)) else 0.0
        obs = self.obs
        info = {}

        return obs, reward, done, info


    def check_game_over(self, player=0):
        
        triangles = False
        
        # iterate over each vertex
        for ii in range(self.num_vertices):
            # list vertices connected to vertex ii
            
            connections = [jj if (not(ii==jj) and self.state[ii,jj,player]) else None\
                    for jj in range(self.num_vertices)]
            while None in connections: connections.remove(None)

            # if any two vertices that are connected to vertex ii\
            # are connected to each other, \
            # that's a triangle (game over)
            triangles = [self.state[elem,elem2,player] \
                    for elem, elem2 in zip(connections, reversed(connections))]
            if np.sum(triangles) > 0:
                triangles = True

        return True


if __name__ == "__main__":

    env = SimEnv()
    for epds in range(10):
        done = False
        obs = env.reset()
        while not done:
            for player in [0,1]:
                action = np.random.choice(env.legal_moves)
                action = env.action_space.sample()
                obs, reward, done, info = env.step(action, player)

                if done:
                    print("player {} loses, congrats player {}".format(\
                            player, int(not(player))))


