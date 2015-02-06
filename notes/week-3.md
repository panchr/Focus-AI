# Week of February 2, 2015

## General Goal: 
Plan data structures of the AI and what type of data it needs to collect

### Reading Topic: 
Dynamic Scripting Data Models

#### Moves Played
Every game, the AI will need to record a list of its played moves. Then, when it receives feedback from the human player, it can modify the weights of these moves.
The weight is increased if the AI seemed human, or decreased otherwise.

##### Rulebase
The rulebase consists of rules. Each rule is defined as follows:

|Name|Data type|Description|
|-------|-----------|-------------|
|Game State|2D Array|This contains the game state that the rule was used for|
|Humanness Weight|Integer|The ever-changing weight of the rule|
|Condition|String|A machine-interpretable condition for the rule|
|Response|String|The response that the AI should take|

When searching for a decision, the AI is essentially searching for the current condition/stimulus with the greatest game-state similarity and the greatest human weight.
This matched rule is then executed and the performance is evaluated.
