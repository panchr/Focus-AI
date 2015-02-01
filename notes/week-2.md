# Week of January 26, 2015

## General Goal: 
Plan structure of the AI and its decision-making process

### Reading Topic: 
General features of game-playing AI

### Notes
I outlined a general [decision-making process](#decision-making-process), which is described below. A few parts are fairly straightforward, but there are also numerous steps that require a bit of data-analysis with ML.
Those steps will require the most amount of time and I will have to read more on this type of data-analysis (generally, categorizing groups of data).
I also labelled groups that are [game-dependent](#game-dependent-features) (and those that aren't). This will allow me to switch games in the future, as long as each game engine shares a certain interface (for movement, getting state, etc). Although I'm going to stick to one game (most likely Checkers), I wanted to make sure that I had this mobility in case I needed it.

### Decision-Making Process

1. AI receives current [state](#game-state) from [game engine](#game-engine)
2. Analyze state to determine possible [stimuli](#stimuli)
3. Based on stimuli, determine possible [response types](#stimuli-response-pairs)
4. Filter rulebase by response and stimuli types
5. From the filtered list, sort rules based on [state similarity](#state-similarity) and [humanness weight](#humanness-weight)
6. Make the most human move from the sorted list ([possible advanced features](#advanced-features))
7. Record the move taken for this game

After each game, the AI does the following:

1. Get the player's feedback on the humanness level
2. Modify each played rule's weight according to this [perceived humanness level](#humanness-weight).

The player is asked whether (s)he thinks the AI is human or an AI. In addition, if the AI did not seem human, I could ask which move gave it away. This move's weight would be reduced further, to help prevent that move from being chosen again.

#### Advanced Features
If I have the time, I want to create a more robust decision-making process. To choose the most human move, the AI would do the following:

1. Choose the top 3 (or 5, depending on speed) responses from the sorted list
2. Simulate the game based on each top response
3. Analyze the humanness level of each simulation, including each step
4. Choose the best move based on these simulations and humanness levels

These features are a lot more complex and I'm not sure if I could actually accomplish them. However, if I have the time, I definitely want to try.

#### Game-Dependent Features

* [Game Engine](#game-engine)
* [Analyzing state for stimuli](#stimuli)
* [Stimuli-Response pairs](#stimuli-response-pairs)
* [State Similarity](#state-similarity)
* [Game simulation (advanced feature that may or may not be included)](#advanced-features)

#### Terms
##### Game State
This is the current state of the game. For example, the state of a game of Checkers can be the game board with pieces and positions labelled.

##### Game-Engine
The game engine is the "driver" of the game. It should enforce the legality of moves as well as control the game mechanics. It should also accept input from two (or more) players, one of which is the AI.
I am hoping to find a pre-existing engine for Checkers, which should not be too hard. If I cannot find an engine that is easy to use, however, I can take a few days to create a basic one.

##### Stimuli
A stimulus is an event that the AI should respond to. Stimuli can be predicted, so it is not required that they have occured already. Examples of [stimuli-response](#stimuli-response-pairs) pairs are shown below. Each response also has a certain [bias](#bias), which affects the extent of the response.

##### Bias
A bias is an advanced feature (so it won't be included initially) that allows the AI to seem more human. The AI can take on a personality (such as being an aggressive or defensive player).
In addition, if the AI can determine the strategy of the opponent (again, such as aggressive or defensive) and then accomodate this determined strategy into its own bias.
Humans naturally have some sort of bias in their responses to stimuli, so this will help make the AI seem more human.

##### Stimuli-Response Pairs
Here are a few examples of possible stimuli and their associated responses. This is just a basic list and it will expand and become more specific as I start working on the actual AI.

|Stimuli Type |Response Type |
|---------------|------------------|
| Threat | Defensive |
| Opening/Weakness | Aggressive |
| Neutral | Neutral |

##### State Similarity
The state similarity is the similarity between two [game states](#game-state). 
One way to implement this is to encode the game board as a string (I got this idea from [a paper on Evolutionary Algorithms](http://ilk.uvt.nl/~pspronck/pubs/PonsenCGAIDE.pdf).) and then compare the strings of the two states, with either regular expressions or some type of fuzzy-string search.

##### Humanness Weight
This is a numeric ranking of the perceived humanness level of the rule. Each rule starts off with the same weight. The weights are increased after each game if the player thinks the AI is human, or lowered if it does not seem human.
As a result, a higher weight is better and so it should be chosen more frequently.
