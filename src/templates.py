actor_template = """
You are an expert in process management.

Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately.

The output must be valid JSON.

This is an example:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']

{{
    result: ['<A>The<A>', '<A>MPON<A>', 'sents', 'the', 'dismissal', 'to', '<A>the<A>', '<A>MPOO<A>', '.']
}}

{input}
"""

activity_template = """
You are an expert in process management.

Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately.

The output must be a valid Python array.

This is an example:

Example input: ['The', 'MPON', 'reports', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.'] 
Example output: ['The', 'MPON', '<A>reports<A>', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.'] 

{input}
"""

activity_data_template = """
You are an expert in process management.

An Activity Data object represents the data or the object directly used by an activity. 
Usually an Activity Data is expressed by a nominal expression (a noun phrase). 
Please annotate the entire noun phrase describing the Activity Data. 
Otherwise, mark the prepositional phrase describing the activity data.

The output must be a valid Python array.

This is an example:

Example input: ['The', 'manager', 'sends', 'the', 'data', 'by', 'email' '.'] 
Example output: ['The', 'manager', 'sends', '<A>the<A>', '<A>data<A>', 'by', 'email' '.'] 

{input}
"""
