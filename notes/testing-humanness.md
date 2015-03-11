## Testing Humanness Levels

To test humanness levels, I decided to go with asking for feedback from the human players.
At the end of every game, the user is asked whether (s)he thought their opponent was an AI or another human.
The user has no prior knowledge, and is not told whether or not their answer is correct.

### Improving AI
Based on this feedback, the server can modify the weights of the rules played that match accordingly.

For example, if the AI did not seem human, then the weights are decreased. However, if it did seem human, the weights are increased.
