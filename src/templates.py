zero_shot_template = """
The input is a list of tokens.

Entity definition:
1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.

If a sequence of tokens matches one of the entities above add a string "<Entity type>" before the first token and add a string "</Entity type>" after the last token.

The output must contain every token that the input contains.

{input}
"""

one_shot_template = """
The input is a list of tokens.

Entity definition:
1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.

If a sequence of tokens matches one of the entities above add a string "<Entity type>" before the first token and add a string "</Entity type>" after the last token.

The output must contain every token that the input contains.

This is an example

["The", "MPON", "sents", "the", "dismissal", "to", "the", "MPOO", "."]

{{
    "data": ["<ACTOR>", "The", "MPON", "</ACTOR>", "<ACTIVITY>", "sents", "</ACTIVITY>", "<ACTIVITY_DATA>", "the", "dismissal", "</ACTIVITY_DATA>", "to", "<ACTOR>", "the", "MPOO", "</ACTOR>", "."]
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
