import numpy as np
import time
from gym import spaces

class SimpleGameEnv():
    def __init__(self):
        pass
    def step(self,action,player):
        pass
    def reset(self):
        num_vertices = 1
        self.state = np.zeros((num_vertices,num_vertices))
        self.legal_moves = [0]
        self.obs = 0
        obs = self.obs

        return obs

    def check_game_over(self):
        game_over = False

        if len(self.legal_moves) == 0:

            game_over=True

        return game_over

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
            # illegel move, edge already taken
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

class TicTacToeEnv(SimpleGameEnv):
    def __init__(self, num_vertices=3):
        self.num_vertices = num_vertices
        self.action_dim = 9 
        self.obs_dim = [self.action_dim, 2]
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)
        self.act_dict = [[int(square/3),square % 3] for square in range(9)]

    def reset(self):
        self.state = np.zeros((self.num_vertices,self.num_vertices,2))
        self.legal_moves = [square for square in range(self.action_dim)]
        obs = self.get_obs()
        return obs

    def get_obs(self):
        return self.state.ravel()

    def step(self, action, player=0):
        try:
            _ = self.legal_moves
        except:
            print("call env.reset before env.step")
            self.reset()

        assert len(self.legal_moves) is not 0, print("game is over, please reset")

        square = self.act_dict[action] 

        if self.state[square[0],square[1],0] \
            or self.state[square[0],square[1],1]:
            illegal = True
            done = True
            print("illegal move attempted by player ", player)
        else:
            illegal = False
            self.state[square[0], square[1], player] = 1.0
            self.legal_moves.remove(action)

        if not illegal:
            win, done = self.check_game_over(player)

            if win:
                reward = 1.0
            else:
                reward = 0.0

        else:
            reward = 0.0          
        info = {}

        obs = self.get_obs()

        return obs, reward, done, info
        
    def check_game_over(self, player):
        win = False


        diag_sums = [0,0]
        for ii in range(3):
            if np.sum(self.state[ii,:,player]) == 3 \
                or np.sum(self.state[:,ii,player]) == 3:
                win = True
                break

            diag_sums[0] += self.state[ii,ii,player]
            diag_sums[1] += self.state[2-ii,2-ii,player]

        if win or 3 in diag_sums:
            win = True
            done = True
        elif len(self.legal_moves) == 0:
            done = True
        else:
            done = False

        return win, done

    def disp_game(self):
        st = self.state

        for hh in range(3):
            print(['x' if st[hh, ii%3,0] else\
                    'o' if st[hh,ii%3,1] else ' '\
                    for ii in range(3)])

        print(' ')

class HexapawnEnv(SimpleGameEnv):

    def __init__(self):
        pass

    def reset(self):
        self.state = np.zeros((3,3))
        self.state[0,:] = 1.0 * np.arange(1,4)
        self.state[2,:] = -1.0 * np.arange(1,4) 
        self.pieces = list(self.state[0,:]).extend(list(self.state[2,:]))
        self.legal_moves = [[ii for ii in range(9)]]
        self.update_legal_moves()
        self.obs = np.sign(self.state.ravel)()
        obs = self.obs

        return obs

    def update_legal_moves(self):
        pass    

    def step(self):
        
        try:
            _ = self.obs
        except:
            print("call env.reset before env.step")
            self.reset()

        assert len(self.legal_moves) is not 0, \
                print("game is over, please reset")
        
        info = {}
        done = False
        obs = self.obs
        reward = 0.0
        return obs, reward, done, info
    

if __name__ == "__main__":

    env = SimEnv()
    for make_env in [TicTacToeEnv]:
        env = make_env()

        for epds in range(10):
            done = False
            obs = env.reset()
            while not done:
                for player in [0,1]:
                    action = np.random.choice(env.legal_moves)
                    obs, reward, done, info = env.step(action, player)
                    if done and reward > 0:
                        print("plyr {} loses, congrats plyr {}".format(\
                                player, int(not(player))))
                        break
                    elif done:
                        print("game is a draw")
                        break
                env.disp_game()


