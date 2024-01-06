actor_template = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately.

The output must be valid JSON.

This is an example:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']

{{
    "result": ['<actor>The<actor>', '<actor>MPON<actor>', 'sents', 'the', 'dismissal', 'to', '<actor>the<actor>', '<actor>MPOO<actor>', '.']
}}

{input}
"""

actor_activity_template = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action. 
If there are multiple actors, annotate each separately.

Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately.

The output must be valid JSON.

This is an example:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']

{{
    "result": ['<actor>The<actor>', '<actor>MPON<actor>', '<activity>sents<activity>', 'the', 'dismissal', 'to', '<actor>the<actor>', '<actor>MPOO<actor>', '.']
}}

{input}
"""

complete_template = """
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

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']

{{
    "result": ['<actor>The<actor>', '<actor>MPON<actor>', '<activity>sents<activity>', '<activity_data>the<activity_data>', '<activity_data>dismissal<activity_data>', 'to', '<actor>the<actor>', '<actor>MPOO<actor>', '.']
}}

{input}
"""

actor_template_extended_example = """
Annotate the entire noun phrase mentioning the actor. 
In this context, an actor is any organizational element responsible for the action.
If there are multiple actors, annotate each separately.

The output must be valid JSON.

This is an example:

[ 'The', 'process', 'starts', 'periodically', 'on', 'the', 'first', 'of', 'each', 'month', ',', 'when', 'Assembler', 'AG', 'places', 'an', 'order', 'with', 'the', 'supplier', 'in', 'order', 'to', 'request', 'more', 'product', 'parts', '.', 'a', ')', 'Assembler', 'AG', 'sends', 'the', 'order', 'to', 'the', 'supplier', '.', 'b', ')', 'The', 'supplier', 'processes', 'the', 'order', '.', 'c', ')', 'The', 'supplier', 'sends', 'an', 'invoice', 'to', 'Assembler', 'AG', '.', 'd', ')', 'Assembler', 'AG', 'receives', 'the', 'invoice', '.' ]

{{
    "result": [ 'The', 'process', 'starts', 'periodically', 'on', 'the', 'first', 'of', 'each', 'month', ',', 'when', 'Assembler', 'AG', 'places', 'an', 'order', 'with', '<A>the<A>', '<A>supplier<A>', 'in', 'order', 'to', 'request', 'more', 'product', 'parts', '.', 'a', ')', '<A>Assembler<A>', '<A>AG<A>', 'sends', 'the', 'order', 'to', '<A>the<A>', '<A>supplier<A>', '.', 'b', ')', '<A>The<A>', '<A>supplier<A>', 'processes', 'the', 'order', '.', 'c', ')', '<A>The<A>', '<A>supplier<A>', 'sends', 'an', 'invoice', 'to', '<A>Assembler<A>', '<A>AG<A>', '.', 'd', ')', '<A>Assembler<A>', '<A>AG<A>', 'receives', 'the', 'invoice', '.' ]
}}

{input}
"""

activity_template = """
Annotate the main activity in the sentence. Include only the verbal or nominal expression of 
the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple 
activities, annotate each separately.

The output must be valid JSON.

This is an example:

['The', 'MPON', 'reports', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.'] 

{{
    "result": ['The', 'MPON', '<activity>reports<activity>', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.'] 
}}

{input}
"""

activity_data_template = """
An Activity Data object represents the data or the object directly used by an activity. 
Usually an Activity Data is expressed by a nominal expression (a noun phrase). 
Please annotate the entire noun phrase describing the Activity Data. 
Otherwise, mark the prepositional phrase describing the activity data.

The output must be valid JSON.

This is an example:

['The', 'manager', 'sends', 'the', 'data', 'by', 'email', '.', 'The', 'office', 'receives', 'an', 'order', 'sent', 'by', 'email', 'from', 'the', 'customer'] 

{{
    "result": ['The', 'manager', 'sends', '<activity_data>the<activity_data>', '<activity_data>data<activity_data>', 'by', 'email', '.', 'The', 'office', 'receives', '<activity_data>an<activity_data>', '<activity_data>order<activity_data>', 'sent', 'by', 'email', 'from', 'the', 'customer'] 
}}

{input}
"""
