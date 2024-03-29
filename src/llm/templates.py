zero_shot_template_base = """
The input is a list of tokens.

Entity definition:
1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.

If a sequence of tokens matches one of the entities above add a string "<Entity type>" before the first token and add a string "</Entity type>" after the last token.

The output must contain every token that the input contains.
The output must be valid JSON.

Now annotate the following text:

{input}
"""

one_shot_template_base = """
The input is a list of tokens.

Entity definition:
1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.

If a sequence of tokens matches one of the entities above add a string "<Entity type>" before the first token and add a string "</Entity type>" after the last token.

The output must contain every token that the input contains.
The output must be valid JSON.

Here is the example:

{example_tokens_1}

{{
    "data": {example_annotations_1}
}}

{input}
"""

few_shot_template_base = """
The input is a list of tokens.

Entity definition:
1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.

If a sequence of tokens matches one of the entities above add a string "<Entity type>" before the first token and add a string "</Entity type>" after the last token.

The output must contain every token that the input contains.
The output must be valid JSON.

Here is the first example:

{example_tokens_1}

{{
    "data": {example_annotations_1}
}}

Here is the second example:

{example_tokens_2}

{{
    "data": {example_annotations_2}
}}

{input}
"""

relation_template = """
If an actor is responsible for an activity mark it as ACTOR-PERFORMER.
If an actor receives data or a trigger from an ACTIVITY mark it as ACTOR-RECIPIENT.

Use the following format to describe the relation between entities:

<startTokenId>,<endTokenId>,<type>,<startTokenId>,<endTokenId>
<startTokenId>,<endTokenId>,<type>,<startTokenId>,<endTokenId>
<startTokenId>,<endTokenId>,<type>,<startTokenId>,<endTokenId>

The input text hast the following format:

<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>

This is an example:

{example_input}

Now annotate the following text:

{input}
"""
