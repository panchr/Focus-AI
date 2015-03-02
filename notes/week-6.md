# Week of February 23, 2015

## General Goal: 
Work on AI's Game state storage (the Gamestate class)

### Switching Storage Types
I originally tried implementing all of my game state storage as bitstrings, because I thought this would be faster than using 2D lists.
However, it turns out that some bitstrings implementations (I suspect `AND`, `OR`, `XOR`, and `NOT` are to blame) are slow because of the number of operations.
The rest of my notes on my experiment with bitstrings are located [here](bitstring.md).

Instead, I ended up switching to 2-dimensional `numpy` matrices. These are easier to use and most likely faster, because they are implemented in C.
My only problem with these will be comparing state similarity, but I will probably do this by concatenating each element of the matrix into a single integer and then finding the difference between the resulting integers of each state.
