# Deep Learning Notes

Representation Learning is a way to detect features and patterns in data. In my case, it can be used to detect game strategies by analyzing gameplay instead of manually creating a list of strategies.

Deep Learning is one of the most common types of Representation Learning. For it to occur, the data must be structured in certain ways.

- Along with neural networks, deep learning made great advances in image, voice, and natural language recognition

A big aspect of representation learning is that it should have domain adaptation --- the features learned from one dataset should be applicable to a similar dataset.

- For this to work, the two tasks/datasets must have some sort of relation
- When set X is similar to set Y, then Task(X) is similar to Task(Y)
- Each feature should be generally explained by smaller features (kind of like axioms)
- Thus, features should build upon each other
- Certain subsets of data share some certain features, but they don't have to share every common features
- Some factors can be related in simple ways (such as the laws of physics)

Ideal learning occurs when the AI can infer patterns from the dataset.
	
- However, this is pretty hard to due and usually, some sort of labelled subset of the data is provided
- In addition, data can be entangled when two different features affect one outcome, so the algorithm should be able to distinguish the two features

Nonlinear feature models are more robust than linear models, but they are also harder to implement and debug.

Potentially, features could be depicted as bitstrings. For example, bitstrings for the row of a checkers game:

*Player A:*

|Position|1|2|3|4|5|6|7|8|
|---------|---|---|---|---|---|---|---|---|
|Occupied?|0|0|1|1|0|1|0|1

*Player B:*

|Position|1|2|3|4|5|6|7|8|
|---------|---|---|---|---|---|---|---|---|
|Occupied?|0|1|0|0|0|0|1|0

Thus, Player 1's bitstring is `00110101` and Player B's bitstring is `01000010`. To check if the board is valid, we can simply do `A AND B`, which is equivalent to `00110101 AND 01000010`. The resulting bitstring should be `00000000` for any given row/column/diagonal.

|Board Function|Logical Equivalent|
|-----------------|----------------------|
|Board is valid|`A AND B`|
|Occupied positions|`A OR B`|
|Unoccipied positions|`NOT (A OR B)`|
