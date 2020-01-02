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
        obs = self.get_obs()

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
        self.obs_dim = [self.action_dim*2]
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)
        self.act_dict = []
        [[self.act_dict.append([jj,ii]) \
                for ii in range(jj+1,self.num_vertices)] \
                for jj in range(self.num_vertices)]

    def reset(self):
        self.state = np.zeros((2,self.num_vertices,self.num_vertices))
        self.legal_moves = [ii for ii in range(self.action_dim)]
        obs = self.get_obs()

        return obs

    def get_obs(self):
        obs = []
        [[[obs.append(self.state[player,ii,jj]) \
                for jj in range(ii+1,self.num_vertices)] \
                for ii in range(self.num_vertices)] \
                for player in [0,1]]

        return np.array(obs)

    def step(self, action, player=0):

        try:
            _ = self.legal_moves
        except:
            print("call env.reset before env.step")
            self.reset()

        assert len(self.legal_moves) is not 0, print("game is over, please reset")

        edge = self.act_dict[action]

        if action in self.legal_moves:
            self.state[player,edge[0], edge[1]] = 1.0
            self.legal_moves.remove(action)
        else:
            # illegel move, edge already taken
            illegal = True
            done = True

        triangles = self.check_game_over(player)

        done = False
        if triangles:
            reward = 0.0
            done = True
        else:
            reward = 1.0 if len(self.legal_moves)==1 else 0.0
            

        done = True if reward == 1.0 else done
        obs = self.get_obs()
        info = {}

        return obs, reward, done, info


    def check_game_over(self, player=0):
        
        has_triangles = False
        
        # iterate over each vertex
        for ii in range(self.num_vertices):
            # list vertices connected to vertex ii
            
            connections = [jj if (not(ii==jj) and self.state[player,ii,jj]) else None\
                    for jj in range(self.num_vertices)]
            while None in connections: connections.remove(None)

            # if any two vertices that are connected to vertex ii\
            # are connected to each other, \
            # that's a triangle (game over)

            #triangles = [self.state[player, elem, elem2] \
            #        for elem, elem2 in zip(connections, reversed(connections))]
            triangles = []
            [[triangles.append(self.state[player,ii,jj] if ii!=jj else 0.0) \
                    for jj in connections] \
                    for ii in connections]
            if np.sum(triangles) > 0:
                has_triangles = True

        return has_triangles

class TicTacToeEnv(SimpleGameEnv):
    def __init__(self, num_vertices=3):
        self.num_vertices = num_vertices
        self.action_dim = 9 
        self.obs_dim = [self.action_dim * 2]
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)
        self.act_dict = [[int(square/3),square % 3] for square in range(9)]

    def reset(self):
        self.state = np.zeros((2,self.num_vertices,self.num_vertices))
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

        if self.state[0,square[0],square[1]] \
            or self.state[1,square[0],square[1]]:
            illegal = True
            done = True
        else:
            illegal = False
            self.state[player, square[0], square[1]] = 1.0
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
            if np.sum(self.state[player,ii,:]) == 3 \
                or np.sum(self.state[player,:,ii]) == 3:
                win = True
                break

            diag_sums[0] += self.state[player,ii,ii]
            diag_sums[1] += self.state[player,2-ii,2-ii]

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
            print(['x' if st[0,hh, ii%3] else\
                    'o' if st[1,hh,ii%3] else ' '\
                    for ii in range(3)])

        print(' ')

class HexapawnEnv(SimpleGameEnv):

    def __init__(self):
        self.action_dim = 9
        self.obs_dim = [self.action_dim*2]
        self.action_space = spaces.Discrete(self.action_dim)
        self.observation_space = spaces.Box(0, 1, shape=self.obs_dim, dtype=np.int16)

    def reset(self):
        self.state = np.zeros((2,3,3))
        self.state[0,0,:] = 1.0 * np.arange(1,4)
        self.state[1,2,:] = 1.0 * np.arange(1,4) 
        self.legal_moves = [[ii for ii in range(9)]] * 2

        self.update_legal_moves()
        obs = self.get_obs()

        return obs

    def update_legal_moves(self):

        self.legal_moves = []
        for player in [0,1]:
            direction = -1 if player else 1
            player_moves = []
            for pawn in [1,2,3]:

                pawn_moves = []
                if pawn in self.state[player,...]:
                    offset =  (pawn-1) * 3 
                    pawn_idx = np.argmax(\
                            np.where(self.state[player,...]==pawn,1,0))
                    coord_x, coord_y = int(pawn_idx/3), pawn_idx % 3

                    if coord_x + direction >= 0 and\
                            coord_x + direction <= 2:
                        if coord_y-1 >= 0:
                            if self.state[1 - player,\
                                coord_x+direction, coord_y-1]:
                                # diagonal capture left
                                pawn_moves.append(offset+0)

                        if not(\
                                self.state[0,coord_x+direction,coord_y])\
                                and not(\
                                self.state[1,coord_x+direction, coord_y]):
                            # diagonal capture left
                            pawn_moves.append(offset+1)

                        if coord_y+1 <=2:
                            if self.state[1-player,\
                                coord_x+direction,coord_y+1]:
                                # diagonal capture left
                                pawn_moves.append(offset+2)


                player_moves.extend(pawn_moves)
            self.legal_moves.append(player_moves) 

    def get_obs(self):
        return np.sign(np.abs(self.state)).ravel()

    def step(self, action, player=0):
        
        try:
            _ = self.legal_moves
        except:
            print("call env.reset before env.step")
            self.reset()

        assert len(self.legal_moves) is not 0, \
                print("game is over, please reset")
        
        if action in self.legal_moves[player]:
            direction = -1 if player else 1
            pawn = 1 + np.floor(action/3) 
            move = action % 3
            pawn_idx = np.argmax(\
                    np.where(self.state[player,...]==pawn,1,0))
            coord_x, coord_y = int(pawn_idx/3), pawn_idx % 3
            self.state[player,coord_x, coord_y] = 0.0

            if move == 0:
                self.state[player,coord_x + direction,coord_y-1] = pawn
                self.state[1-player,coord_x + direction,coord_y-1] = 0.0
            elif move == 1:
                self.state[player,coord_x + direction,coord_y] = pawn
            elif move == 2:
                self.state[player,coord_x + direction,coord_y+1] = pawn
                self.state[1-player,coord_x + direction,coord_y+1] = 0.0
        else:
            illegal = True
            done = True

        self.update_legal_moves()
        win, done = self.check_game_over(player)

        reward = 1.0 if win else 0.0
        info = {}

        obs = self.get_obs()

        return obs, reward, done, info

    def check_game_over(self,player=0):

        if len(self.legal_moves[1-player]) == 0:
            # if opponent is unable to move
            win, done = True, True
        elif self.state[player, 2-player*2,:].any():
            # if player moves pawn to final opposing row
            win, done = True, True
        else:
            # game continues
            win, done = False, False


        return win, done

    def disp_game(self):
        st = self.state
        for hh in range(3):
            print(['x' if st[0,hh, ii%3] else\
                    'o' if st[1,hh,ii%3] else ' '\
                    for ii in range(3)])

        print(' ')

    

if __name__ == "__main__":

    env = SimEnv()
    for ii in range(100):
        done = False
        env.reset()
        steps = 0
        while not done:
            for player in [0,1]:
                obs, reward, done, info = env.step(np.random.choice(env.legal_moves),player)
                steps += 1
                if done:
                    print("player {}".format(player))
                    print("game over after {} moves, reward {}"\
                            .format(steps,reward))
                    break
#    for make_env in [HexapawnEnv, TicTacToeEnv, SimEnv ]:
#        env = make_env()
#
#        for epds in range(3):
#            done = False
#            obs = env.reset()
#            while not done:
#                for player in [0,1]:
#                    env.disp_game()
#                    if type(env.legal_moves[0]) == list:
#                        legal_moves = env.legal_moves[player]
#                    else:
#                        legal_moves = env.legal_moves
#                    action = np.random.choice(legal_moves)
#                    obs, reward, done, info = env.step(action, player)
#                    if done and reward > 0:
#                        print("plyr {} loses, congrats plyr {}".format(\
#                                player, int(not(player))))
#                        break
#                    elif done and reward < 0:
#                        print("plyr {} loses, congrats plyr {}".format(\
#                                int(not(player)),player))
#                        break
#
#                    elif done:
#                        print("game is a draw")
#                        break
#                print(reward)


