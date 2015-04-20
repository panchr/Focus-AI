*Here are my guiding questions. Similar to my timeline, these are flexible and may change if necessary.*

## Overall Question

### How can a game-playing AI be developed such that it is indistinguishable from a human player?

## Guiding Questions

1. What games are suitable and practical for such an AI?
2. What features must a human-like game-playing AI implement?
3. What types of data does the AI need to gather for its learning process?
4. How will the AI learn?
	1. In addition to modifying rule weights, can the AI dynamically generate new rules?
5. How can the AI's humanness level be tested?
	1. Can the data gathered from the tests be used to further improve the AI, and if so, how?
6. How can such an AI be implemented using Python? 
	1. To store the data, will a robust relational database backend (such as MySQL or PostgreSQL) be required, or is a NoSQL/document database (such as MongoDB) adequate?
	2. How can a suitable game engine be developed in Python?
	3. How will the AI interact with a game engine?
7. What type of interface will the primary application be?
	1. If using a web-based interface, how will the website interface with the AI and game engine?
	2. How can a Python-driven AI support concurrent connections?
	3. Can each connection (and respective AI instance) remain isolated from the rest?
