# RL Simple Games
A collection of gratingly simple mathematical/board games implemented as reinforcement learning environments. These games were chosen for being relatively easy to learn and iterate on and in general have solutions for optimal gameplay.


## Tic-Tac-Toe (aka Noughts and Crosses)
NaC is a simple game with 9 boxes separated by 4 lines. 2 Players alternate placing an 'X' or an 'O,' respectively, into one of the remaining unoccupied boxes until one of the players has created a row, column, or diagonal streak of 3 of their symbols. Perfect play from both players results in a draw. Ok I know that you know what tic-tac-toe is (and that you know that I know that you know) but anyway you can read the Wikipedia page for [more](https://en.wikipedia.org/wiki/Tic-tac-toe)

```
[' ', ' ', ' ']
[' ', ' ', ' ']
[' ', ' ', ' ']

[' ', ' ', ' ']
[' ', ' ', ' ']
[' ', ' ', 'x']

0.0
[' ', ' ', ' ']
[' ', ' ', ' ']
[' ', 'o', 'x']

[' ', ' ', ' ']
['x', ' ', ' ']
[' ', 'o', 'x']

0.0
[' ', 'o', ' ']
['x', ' ', ' ']
[' ', 'o', 'x']

['x', 'o', ' ']
['x', ' ', ' ']
[' ', 'o', 'x']

0.0
['x', 'o', ' ']
['x', ' ', 'o']
[' ', 'o', 'x']

plyr 0 loses, congrats plyr 1
['x', 'o', ' ']
['x', 'x', 'o']
[' ', 'o', 'x']

1.0
```
## Sim
Sim is a graph-building game where the objective is to avoid creating a monochromatic triangle. Six vertices make up the realm-of-play and players take turns connecting unconnected vertices with their unique and identifying color. If a player creates a triangle with all 3 edges the same color, they lose, so the goal is to force one's opponent to complete a triangle (passing a turn is not allowing, natch). There are 15 possible edges (the graph is undirected) and perfect play leads to a win for player 2. 

Sim is currently the hardest game in the simple-games suite, and the graph is represented as two matrices (one for each palyer) with active gameplay edges represented above the diagonal as '1.0' and all other elements '0.0' Sim is a [Ramsey game](https://en.wikipedia.org/wiki/Ramsey_theory) and a draw is impossible as follows from the [Theorem on friends and strangers`](https://en.wikipedia.org/wiki/Theorem_on_friends_and_strangers)` 


```
plyr 1 loses, congrats plyr 0
[[[0. 0. 1. 1. 0. 1.]
  [0. 0. 1. 0. 1. 1.]
  [0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 1. 0.]
  [0. 0. 0. 0. 0. 0.]
  [0. 0. 0. 0. 0. 0.]]

 [[0. 1. 0. 0. 1. 0.]
  [0. 0. 0. 1. 0. 0.]
  [0. 0. 0. 1. 1. 0.]
  [0. 0. 0. 0. 0. 1.]
  [0. 0. 0. 0. 0. 1.]
  [0. 0. 0. 0. 0. 0.]]]
``` 

### Hexapawn 
Hexapawn was a game that was invented because tic-tac-toe was too complex. It was introduced by Martin Gardner in his column for Scientific American <em>Mathematical Games</em> to allow readers a chance to implement a game learner in matchboxes, based on the noughts and crosses engine [MENACE](https://en.wikipedia.org/wiki/Donald_Michie#Career_and_research). A draw is impossible, because the first player unable to move loses, and like Sim the second player apparently has the advantage. 


```                       
['x', 'x', 'x']
[' ', ' ', ' ']
['o', 'o', 'o']

['x', ' ', 'x']
[' ', 'x', ' ']
['o', 'o', 'o']

0.0

['x', ' ', 'x']      
['o', 'x', ' ']        
[' ', 'o', 'o']      
                     
['x', ' ', ' ']      
['o', 'x', 'x']       
[' ', 'o', 'o']        
                      
0.0                  
['x', ' ', ' ']      
['o', 'o', 'x']      
[' ', 'o', ' ']      
                       
[' ', ' ', ' ']              
['o', 'x', 'x']        
[' ', 'o', ' ']      
                     
0.0                  
[' ', ' ', ' ']       
['o', 'x', 'o']      
[' ', ' ', ' ']        
                      
plyr 0 loses, congrats plyr 1
[' ', ' ', ' ']
['o', ' ', 'o']
[' ', 'x', ' ']

1.0

```
