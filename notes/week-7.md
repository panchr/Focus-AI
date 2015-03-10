# Week of March 2, 2015

## General Goal: 
Work on Checkers Game Engine and finish converting 

### Notes
I started the week by finishing converting all of the `Gamestate` methods to use 2-D `numpy` arrays.
This proved to be much easier than using bitstrings and (surprisingly) faster.

Each player is represented as an integer, and a player's King is negated.
For example, Player 1's normal pieces are represented with `1` and his/her Kings are represented with `-1`.

Right now, game state comparisons do not keep track of the original matrix positions.

I started to search for a Checkers game engine, implemented in Python, but I could not find any.
Instead, I found Checkers game clients, but these were no use to me.

So, I started to develop my own. This was relatively easy, until I started dealing with the "intricate" parts of Checkers: validating moves and taking pieces.

#### Validating Moves
The main function of any game engine is move validation and execution - if a move appears to be valid, then execute the move.
There are two types of moves in Checkers, which I labelled as "simple" and "taking" moves.

##### Simple Move Conditions
A "simple" move is when a piece is being moved normally. It is valid under the following conditions:

* Old position is in {-2, -1, 1, 2}
* New position is 0
* Move is diagonal (absolute change in `x` and `y` are both 1)
* If Player 1, then change in `y` is positive, otherwise it's negative (irrelevant if a King is being moved)

##### Taking Move Conditions
A "taking" move is when a piece is taking the opponent's pieces. It is valid under the following conditions:

* Old position is in {-2, -1, 1, 2}
* New position is 0
* Move is diagonal (absolute change in `x` and `y` are even)
* If Player 1, then change in `y` is positive, otherwise it's negative (irrelevant if a King is being moved)
* There is a diagonal (zig-zags allowed) path between the start and end positions
* In this diagonal path, each set of two squares should be of the following order: {open, enemy piece}

I have not fully implemented the "taking" move validation nor the mechanism for taking pieces (but these two will work together, so this should be simple).

### Core Interaction
Because both the AI core and Game Engine are written in Python, interaction between the two will be simple: the core runner will simply contain an`Engine` instance.
