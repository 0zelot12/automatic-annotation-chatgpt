# Simple Actor

Given this ruleset:

1. Annotate the entire noun phrase mentioning the actor. In this context, an actor is any organizational element responsible for the action. If there are multiple actors, annotate each separately.

2. Annotate the entire noun phrase mentioning the actor.

3. There can be multiple actors in one sentence.

The Coordination Unit of the Company A sends the report to the Coordination Unit of the Company B.

# Simple Activity

Given this definition:

1. An Activity is a single unit of work performed in a process. If there are multiple activities, annotate each separately.

2. An Activity mark should mark only the expression (either verbal or nominal) expressing the activity.

3. Do not include in the annotation mark the activity object used by the activity.

4. Exclude from the annotation mark articles, and conjunctions that are at the boundary of the annotation span.

ABC Company transmits the data to Company B.

<--> 
Identify and annotate the main activity in the sentence. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple activities, annotate each separately.
<--> 

# Simple activity data

Given this definition:

An Activity Data object represents the data or the object directly used by an activity. Usually an Activity Data is expressed by a nominal expression (a noun phrase). Please annotate the entire noun phrase describing the Activity Data. Otherwise, mark the prepositional phrase describing the activity data. Underline the annotation in the output.

Anotate the following sentence using the definition provided above:

The client sends a message to the customer.

# Actor + Activity + Activity Data

## Definition actor

Annotate the entire noun phrase mentioning the actor. In this context, an actor is any organizational element responsible for the action. If there are multiple actors, annotate each separately.

## Definition activity

Identify and annotate the main activity in the sentence. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple activities, annotate each separately.

## Definition activity data

An Activity Data object represents the data or the object directly used by an activity. Usually an Activity Data is expressed by a nominal expression (a noun phrase). Please annotate the entire noun phrase describing the Activity Data. Otherwise, mark the prepositional phrase describing the activity data. Underline the annotation in the output.

## Definition AND Gateway

## Definition XOR Gateway

## Definition Condition Specicifaction

## Defintion Further Specification

## Definition O

# Output format

{
    actors: ["Actor 1", "Actor 2"],
    activities: ["Activity 1", "Activity 2"],
    activity_data: ["Activity Data 1", "Activity Data 2"]
}
