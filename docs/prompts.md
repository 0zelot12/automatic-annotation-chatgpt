# Definition Actor

Annotate the entire noun phrase mentioning the actor. In this context, an actor is any organizational element responsible for the action. If there are multiple actors, annotate each separately.

This is an example:

['The', 'MPON', 'sents', 'the', 'dismissal', 'to', 'the', 'MPOO', '.']
{ actors: ["The MPON", "the GO"] }

# Definition Activity

Annotate the main activity in the sentence. Include only the verbal or nominal expression of the activity, excluding any objects, prepositional phrases, articles, or conjunctions. If there are multiple activities, annotate each separately.

This is an example:

['The', 'MPON', 'reports', 'the', 'meter', 'operation', 'to', 'the', 'GO', '.']
{ activties: ["reports"] }

# Definition Activity Data

An Activity Data object represents the data or the object directly used by an activity. Usually an Activity Data is expressed by a nominal expression (a noun phrase). Please annotate the entire noun phrase describing the Activity Data. Otherwise, mark the prepositional phrase describing the activity data.

['The', 'manager', 'sends', 'the', 'data', 'by', 'email' '.']
{ activity_data: ["the data"] }

# Definition AND Gateway

A gateway represents a control flow point in a process model where the process flow is split into alternative paths, or whether multiple possible paths are merged (aka joined).

An AND split or parallel split is a point in a process model where a single thread of control splits into multiple threads of control which are executed concurrently.

# Definition XOR Gateway

# Definition Condition Specicifaction

# Defintion Further Specification

The Further Specification layer captures important details of an Activity, such as the mean or the manner of its execution. Please include the opening preposition in the annotation mark, if present.

['The', 'database', 'is', 'checked', 'to', 'see', 'whether', 'the', 'table', 'has', 'new', 'records.']
{ further_specifications: ["to see whether the table has new records"] }

# Definition O
 
-> TODO

# Example sentences

## Plaintext

The MPON sents the dismissal to the MPOO.
The MPOO reviews the dismissal.
The EC tells the INQ about the change of his master data.

## Array

["The", "MPON", "sents", "the", "dismissal", "to", "the", "MPOO", "."]
["The", "MPOO", "reviews", "the", "dismissal", "."]
["The", "EC", "tells", "the", "INQ", "about", "the", "change", "of", "his", "master", "data", "."]
