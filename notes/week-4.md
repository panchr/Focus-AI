# Week of February 9, 2015

## General Goal: 
Develop data structures and research dynamic rule generation

### Reading Topic: 
Using evolutionary algorithms to generate Dynamic Scripting rules

#### Data Structures
I started working on the data structures. I created a general model of each rule in the rulebase.
As of now, it is pretty basic basic because I haven't researched enough about the dynamic rule generation.

Here is the current model, built using [Mongokit](https://github.com/namlook/mongokit/wiki) (for MongoDB):

```python
import mongokit
class Rule(mongokit.Document):
	'''A general model for a Dynamic Scripting Rule'''
	__database__ = "senior_focus"
	__collection__ = "rulebase"

	structure = {
		"state": basestring,
		"weight": int,
		"condition": basestring,
		"response": basestring,
		}
	
	required_fields = ["state", "weight", "condition", "response"]
```

*Note: most of my code and development work is the `dev` branch. I will merge it into the `master` branch every week, so the weekly tag will contain the latest development work.*
