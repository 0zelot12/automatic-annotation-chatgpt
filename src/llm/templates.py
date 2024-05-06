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

1. ACTOR_PERFORMER: If an actor is responsible for an activity mark it as ACTOR_PERFORMER.
2. ACTOR_RECIPIENT: If an actor receives data or a trigger from an ACTIVITY mark it as ACTOR_RECIPIENT.
3. FURTHER_SPECIFICATION: If there are important details of an ACTIVITY mark it as FURTHER_SPECIFICATION and link it to its ACTIVITY.
4. USES: If ACTIVITY_DATA is an object or data that is used by an ACTIVITY. 
5. FLOW: A Flow object is a directional connector between activities in a Process. It defines execution order all ACTIVITY entities.
6. SAME_GATEWAY: The SAME_GATEWAY feature allows to connect all parts describing the same gateway, since its description may span over multiple sentences. This means that only gateway elements can be connected by this relation.

Use the following format to describe the relation between entities:

<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>

The input text hast the following format:

<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>

This is an example:

{training_data}

Now annotate the following text:

{test_data}
"""

relation_template_gold_standard = """

Entity definitions:

1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.
4. FURTHER_SPECIFICATION: The Further Specification layer captures important details of an Activity, such as the mean or the manner of its execution.
5. AND_GATEWAY: An AND_GATEWAY is a point in a process model where a single thread of control splits into multiple threads of control which are executed concurrently.
6. XOR_GATEWAY: An XOR_GATEWAY is a point in a process model where one of several branches is chosen.
7. CONDITION_SPECIFICATION: A CONDITION_SPECIFICATION element specifies the condition that must be satisfied by a process instance in order to be allowed to take a particular branch of a control point. Therefore, this process element is always bound with an XOR_GATEWAY.

Relation definitions:

1. ACTOR_PERFORMER: If an actor is responsible for an activity mark it as ACTOR_PERFORMER.
2. ACTOR_RECIPIENT: If an actor receives data or a trigger from an ACTIVITY mark it as ACTOR_RECIPIENT.
3. FURTHER_SPECIFICATION: If there are important details of an ACTIVITY mark it as FURTHER_SPECIFICATION and link it to its ACTIVITY.
4. USES: If ACTIVITY_DATA is an object or data that is used by an ACTIVITY. 
5. FLOW: A Flow object is a directional connector between activities in a Process. It defines execution order all ACTIVITY entities.
6. SAME_GATEWAY: The SAME_GATEWAY feature allows to connect all parts describing the same gateway, since its description may span over multiple sentences. This means that only gateway elements can be connected by this relation.

Use the following format to describe the relation between entities:

<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>,<relationtype>,<entityType>,<startTokenId>,<endTokenId>

The input text has the following format:

<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>

The entities present in the text have the following format:

<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>

This is an example:

{training_data}

Now annotate the following text:

{test_data}
"""

entity_template = """

Entity definitions:

1. ACTOR: Any organizational element responsible for the action. Include the whole noun phrase including articles.
2. ACTIVITY: The main activity in the text. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions.
3. ACTIVITY_DATA: Object representing the data or the object directly used by an activity.
4. FURTHER_SPECIFICATION: The Further Specification layer captures important details of an Activity, such as the mean or the manner of its execution.
5. AND_GATEWAY: An AND_GATEWAY is a point in a process model where a single thread of control splits into multiple threads of control which are executed concurrently.
6. XOR_GATEWAY: An XOR_GATEWAY is a point in a process model where one of several branches is chosen.
7. CONDITION_SPECIFICATION: A CONDITION_SPECIFICATION element specifies the condition that must be satisfied by a process instance in order to be allowed to take a particular branch of a control point. Therefore, this process element is always bound with an XOR_GATEWAY.

Use the following format to describe the entities:

<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>
<entityType>,<startTokenId>,<endTokenId>

The input text has the following format:

<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>
<token>$<tokenId>

This is an example:

{training_data}

Now annotate the following text:

{test_data}
"""
