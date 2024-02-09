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

['A', 'customer', 'brings', 'in', 'a', 'defective', 'computer', 'and', 'the', 'CRS', 'checks', 'the', 'defect', 'and', 'hands', 'out', 'a', 'repair', 'cost', 'calculation', 'back', '.', 'If', 'the', 'customer', 'decides', 'that', 'the', 'costs', 'are', 'acceptable', ',', 'the', 'process', 'continues', ',', 'otherwise', 'she', 'takes', 'her', 'computer', 'home', 'unrepaired', '.', 'The', 'ongoing', 'repair', 'consists', 'of', 'two', 'activities', ',', 'which', 'are', 'executed', ',', 'in', 'an', 'arbitrary', 'order', '.', 'The', 'first', 'activity', 'is', 'to', 'check', 'and', 'repair', 'the', 'hardware', ',', 'whereas', 'the', 'second', 'activity', 'checks', 'and', 'configures', 'the', 'software', '.', 'After', 'each', 'of', 'these', 'activities', ',', 'the', 'proper', 'system', 'functionality', 'is', 'tested', '.', 'If', 'an', 'error', 'is', 'detected', 'another', 'arbitrary', 'repair', 'activity', 'is', 'executed', ',', 'otherwise', 'the', 'repair', 'is', 'finished', '.' ]

{{
    "data": ['<actor>A', 'customer</actor>', '<activity>brings', 'in</activity>', 'a', 'defective', 'computer', 'and', '<actor>the', 'CRS</actor>', '<activity>checks</activity>', '<activity_data>the', 'defect</activity_data>', 'and', '<activity>hands', 'out</activity>', '<activity_data>a', 'repair', 'cost', 'calculation</activity_data>', 'back', '.', 'If', 'the', 'customer', 'decides', 'that', 'the', 'costs', 'are', 'acceptable', ',', 'the', 'process', 'continues', ',', 'otherwise', '<actor>she</actor>', '<activity>takes</activity>', '<activity_data>her', 'computer</activity_data>', '.', 'The', 'ongoing', 'repair', 'consists', 'of', 'two', 'activities', ',', 'which', 'are', 'executed', ',', 'in', 'an', 'arbitrary', 'order', '.', 'The', 'first', 'activity', 'is', 'to', '<activity>check</activity>', 'and', '<activity>repair</activity>', '<activity_data>the', 'hardware</activity_data>', ',', 'whereas', 'the', 'second', 'activity', '<activity>checks</activity>', 'and', '<activity>configures</activity>', '<activity_data>the', 'software</activity_data>', '.', 'After', 'each', 'of', 'these', 'activities', ',', '<activity_data>the', 'proper', 'system', 'functionality</activity_data>', 'is', '<activity>tested</activity>', '.', 'If', 'an', 'error', 'is', 'detected', '<activity_data>another', 'arbitrary', 'repair', 'activity</activity_data>', 'is', '<activity>executed</activity>', ',', 'otherwise', 'the', 'repair', 'is', 'finished', '.']
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
    "data": ['<actor>The<actor>', '<actor>MPON<actor>', '<activity>sents<activity>', '<activity_data>the<activity_data>', '<activity_data>dismissal<activity_data>', 'to', '<actor>the<actor>', '<actor>MPOO<actor>', '.']
}}

['A', 'customer', 'brings', 'in', 'a', 'defective', 'computer', 'and', 'the', 'CRS', 'checks', 'the', 'defect', 'and', 'hands', 'out', 'a', 'repair', 'cost', 'calculation', 'back', '.']

{{
    "data": ['<actor>A<actor>', '<actor>customer<actor>', '<activity>brings<activity>', '<activity>in<activity>', 'a', 'defective', 'computer', 'and', '<actor>the<actor>', '<actor>CRS<actor>', '<activity>checks<activity>', '<activity_data>the<activity_data>', '<activity_data>defect<activity_data>', 'and', '<activity>hands<activity>', '<activity>out<activity>', '<activity_data>a<activity_data>', '<activity_data>repair<activity_data>', '<activity_data>cost<activity_data>', '<activity_data>calculation<activity_data>', 'back', '.']
}}

{input}
"""
