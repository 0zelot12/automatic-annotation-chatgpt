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

Entity definitions:

1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.
4. FURTHER_SPECIFICATION: The Further Specification layer captures important details of an Activity, such as the mean or the manner of its execution.
5. AND_GATEWAY: An AND_GATEWAY is a point in a process model where a single thread of control splits into multiple threads of control which are executed concurrently.
6. XOR_GATEWAY: An XOR_GATEWAY is a point in a process model where one of several branches is chosen.
7. CONDITION_SPECIFICATION: A CONDITION_SPECIFICATION element specifies the condition that must be satisfied by a process instance in order to be allowed to take a particular branch of a control point. Therefore, this process element is always bound with an XOR_GATEWAY.

Relation definitions:

1. ACTOR_PERFOMER: If an actor is responsible for an activity mark it as ACTOR_PERFORMER.
2. ACTOR_RECIPIENT: If an actor receives data or a trigger from an ACTIVITY mark it as ACTOR_RECIPIENT.
3. FURTHER_SPECIFICATION: If there are important details of an ACTIVITY mark it as FURTHER_SPECIFICATION and link it to its ACTIVITY.
4. USES: If ACTIVITY_DATA is an object or data that is used by an ACTIVITY. 
5. FLOW: A Flow object is a directional connector between activities in a Process. It defines execution order all ACTIVITY entities.
6. SAME_GATEWAY: The SAME_GATEWAY feature allows to connect all parts describing the same gateway, since its description may span over multiple sentences. This means that only gateway elements can be connected by this relation.

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
