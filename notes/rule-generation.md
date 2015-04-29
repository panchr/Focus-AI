## Rule Generation

I attempted to research Deep Learning to automatically generate the ruleset based on Checkers gameplay data.
However, this turned out to be a difficult task because Deep Learning is very hard to understand, and I was unable to find any significant gameplay data.

Instead, I decided to create my own ruleset. This was not too hard, except I realized my stimulus analysis (which figures out what conditions are matched in a given game state) enforces the position of moves.
For example, if the game board looked like this:

```python
[0, 1, 0, 1, 0, 1, 0, 1]
[1, 0, 1, 0, 1, 0, 1, 0]
[0, 1, 0, 0, 0, 1, 0, 1]
[0, 0, 1, 0, 0, 0, 0, 0]
[0, 2, 0, 0, 0, 0, 0, 0]
[0, 0, 2, 0, 2, 0, 2, 0]
[0, 2, 0, 2, 0, 2, 0, 2]
[2, 0, 2, 0, 2, 0, 2, 0]
```

There is the possibly for the AI, playing as piece 2, to take player 1's piece. However, if the stimulus looks like:

```python
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]
[0, 1, 0, 0, 0, 0, 0, 0]
[2, 0, 0, 0, 0, 0, 0, 0]
```

The positions of the conditions don't match. Thus, the stimulus would not match and the move would not be executed.
I considered trying to modify my algorithm to match any position. However, I realized this would be difficult to implement.

Instead, I created a [relatively small script](../ai/generate-rules.py) that uses matrix transformations to create translated and reflected versions of each rule.
This enables the AI to find any variation of a rule while still using a relatively simple stimulus analysis algorithm.

All of the matrix transformations were made trivial through the use of `numpy` --- functions like `numpy.roll` and `np.where` help me translate matrices and select certain pieces very easily.
In addition, I can manipulate the matrix very quickly, so this made me even more glad that I did not use bitstrings.

In addition to just varying the positioning and reflections of the rules, I also needed to consider king-based moves. This was also relatively simple through the use of `numpy`.

Once I generated the rules, I had to make sure each rule was valid. This was fairly simple, as I had created a move validation tool for the game engine.
