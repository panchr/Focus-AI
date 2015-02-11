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

I am still working on it so this snippet will soon be out-of-date.

#### Dynamically Generating Rules

I read this interesting paper on [ordering the rulebase in a Dynamic Scripting implementation](http://www.aaai.org/Papers/AIIDE/2007/AIIDE07-009.pdf).
In Spronck's original description of his Dynamic Scripting algorithm, the programmer has to dictate the rule order.
Initially, I planned on having this automated to begin with. I was going to order the AI rules based on the humanness weight --- this seemed intuitive to me.
Indeed, Timuri discusses the weight-based ordering. However, he also looks into two other types of sorting, based on the relationships between two rules, which is the outcome when used together.

I found the relation-based ordering pretty interesting, but it seems fairly complex, at least for now. Maybe if I have time towards the end of my project I will work on learning more about how it works and try implementing it.
