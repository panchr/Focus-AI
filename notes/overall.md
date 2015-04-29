# Overall Planning/Notes

## Last Updated: 4/29/2015

### Current Status

Currently, I am trying to get more players for my game so that my AI can collect data.

### Decision Making Process

1. AI receives current state from game-engine
2. Analyze state to determine possible stimuli
3. Based on stimuli, determine possible response types
4. Filter rulebase by response and stimuli types
5. From the filtered list, sort rules based on state-similarity and humanness weight
6. Make the most human move from the sorted list ([possible advanced features](#advanced-features))
7. Record the move taken for this game

After each game, the AI does the following:

1. Get the player's feedback on the humanness level
2. Modify each played rule's weight according to this perceived humanness weight

The player is asked whether (s)he thinks the AI is human or an AI. In addition, if the AI did not seem human, I could ask which move gave it away. This move's weight would be reduced further, to help prevent that move from being chosen again.

#### Advanced Features
If I have the time, I want to create a more robust decision-making process. To choose the most human move, the AI would do the following:

1. Choose the top 3 (or 5, depending on speed) responses from the sorted list
2. Simulate the game based on each top response
3. Analyze the humanness level of each simulation, including each step
4. Choose the best move based on these simulations and humanness levels

These features are a lot more complex and I'm not sure if I could actually accomplish them. However, if I have the time, I definitely want to try.

### Data Models
The AI needs to collect the game state of every game played. In addition, it should keep track of all the moves played per game.
Each rule in the rulebase should have a unique condition (which triggers it), as well as an associated response, game state, and humanness weight.

When a move seems human, that rule's weight is increased. If it seems like an AI, then the weight is decreased, so that it is less likely to be chosen in the future.

Currently, the game state is stored as a 2-dimensional `numpy.ndarray`, which turned out to be faster than numeric bitstrings.

### Representation Learning
Here are [my notes on representation learning](representation-learning.md).

### Game Engine
I could not find a suitable Checkers Game Engine in Python, so I am working on creating my own. Most of my notes were taken during [week 7](week-7.md).

### Unit testing
My notes on unit tests are located [here](unit-tests.md).
