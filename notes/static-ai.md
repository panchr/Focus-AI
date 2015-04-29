## Static Move Generation

I quickly realized that I could not simply use Dynamic Scripting in my Artificial Intelligence. For example, if a suitable rule is not found, then the AI would hit a barrier and be unable to respond to the game.

To solve this problem, I used a generic search algorithm. First, it starts by finding all of the AI's pieces that still have open adjacent tiles.
Then, it starts by searching all of these open tiles for a possible "take" move. This implements a very basic heuristic: if a take move is found, there is no need to search for a simple move.
I based that idea on the fact that take moves are almost always stronger than regular moves.

If take moves are found, they are ranked based on how many pieces are taken. Simple moves are generally considered to be equally weighted (although I could implement a stronger evaluation technique) so I don't sort these.

Then, the AI goes through each of the moves and tries to execute them. The search only returns valid moves, but I still try every move successively if the first move fails to be valid. Once a move is executed, a stimulus is extracted from the move and it is recorded as a new rule. This prevents the AI from having to repeat the search in a similar scenario.

This has worked pretty nicely, though it could be improved. Namely, the AI makes some relatively stupid mistakes sometimes, mostly because many groups have the same weight.
I am considering indexing the rules by a pre-determined "strength", but this would require a triple-attribute-sort (instead of just two attributes as of now) and I'm not sure if that will work out or how I would go about implementing it.
