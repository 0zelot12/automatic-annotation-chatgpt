one_shot_template = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately.

Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately.

An Activity Data object represents the data or the object directly used by an activity. 
Usually an Activity Data is expressed by a nominal expression (a noun phrase). 

The output must be valid JSON.

This is an example:

['A', 'customer', 'brings', 'in', 'a', 'defective', 'computer', 'and', 'the', 'CRS', 'checks', 'the', 'defect', 'and', 'hands', 'out', 'a', 'repair', 'cost', 'calculation', 'back', '.']

{{
    "result": ['<actor>A customer</actor>', '<activity>brings in</activity>', 'a', 'defective', 'computer', 'and', '<actor>the CRS</actor>', '<activity>checks</activity>', '<activity_data>the defect</activity_data>', 'and', '<activity>hands out</activity>', '<activity_data>a repair cost calculation</activity_data>', 'back', '.']
}}

{input}
"""

few_shot_template = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately. Annotate each token of the noun phrase seperately.

Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately. Annotate each token of the noun phrase seperately.

An Activity Data object represents the data or the object directly used by an activity. 
Usually an Activity Data is expressed by a nominal expression (a noun phrase). Annotate each token of the noun phrase seperately.

The output must be valid JSON.

Here are two examples:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']

{{
    "result": ['<actor>The<actor>', '<actor>MPON<actor>', '<activity>sents<activity>', '<activity_data>the<activity_data>', '<activity_data>dismissal<activity_data>', 'to', '<actor>the<actor>', '<actor>MPOO<actor>', '.']
}}

['A', 'customer', 'brings', 'in', 'a', 'defective', 'computer', 'and', 'the', 'CRS', 'checks', 'the', 'defect', 'and', 'hands', 'out', 'a', 'repair', 'cost', 'calculation', 'back', '.']

{{
    "result": ['<actor>A<actor>', '<actor>customer<actor>', '<activity>brings<activity>', '<activity>in<activity>', 'a', 'defective', 'computer', 'and', '<actor>the<actor>', '<actor>CRS<actor>', '<activity>checks<activity>', '<activity_data>the<activity_data>', '<activity_data>defect<activity_data>', 'and', '<activity>hands<activity>', '<activity>out<activity>', '<activity_data>a<activity_data>', '<activity_data>repair<activity_data>', '<activity_data>cost<activity_data>', '<activity_data>calculation<activity_data>', 'back', '.']
}}

{input}
"""
