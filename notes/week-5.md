# Week of February 16, 2015

## Original Goal: 
Create basic rules for Checkers rulebase

## Modified Goal:
Start working in AI core

### Switching Goals
Originally, I had planned to work on start creating the sets of rules for the AI. This would be for the Dynamic Scripting rulebase.
However, I realized that it might be easier to do so once I know exactly how the AI will work.
So, I decided to work on the rulebase after the core AI features have been developed.
In the meanwhile, I will continue reading about Deep Learning. I am also working with Ethan Holly, a former graduate of my highschool who has studied Representation/Deep Learning in depth, so that I can understand it better. Hopefully by the time the AI core is finished, I will know enough about Deep Learning to dynamically generate the ruleset with data.
I could also change the game to more advanced games, such as Chess or even RTS (real-time strategy) games if the learning algorithm works well enough.

### Rule Database
I decided to use MongoDB as the database for the AI's ruleset, mainly because it's fairly easy to use.
I've used SQL-driven databases before (mostly MySQL), but I recently found and started using MongoDB. 
The storage structure is essentially JSON and there is no enforced schema, so changes are easily applied.
I will need to quickly change the structure of each rule as I develop the AI and determine the needs of the rulebase.
