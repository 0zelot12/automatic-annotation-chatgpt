actor_template = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately.

This is an example:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']
actors: ["The MPON", "the MPOO"]

{input}
"""

activity_template = """Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately.

This is an example:

['The', 'MPON', 'reports', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.'] 
activities: ["reports"]

{input}
"""

activity_data_template = """
An Activity Data object represents the data or the object directly used by an activity. 
Usually an Activity Data is expressed by a nominal expression (a noun phrase). 
Please annotate the entire noun phrase describing the Activity Data. 
Otherwise, mark the prepositional phrase describing the activity data.

This is an example:

['The', 'manager', 'sends', 'the', 'data', 'by', 'email' '.'] 
activity_data: ["the data"]

{input}
"""