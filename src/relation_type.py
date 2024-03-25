from enum import Enum


class RelationType(Enum):
    ACTOR_PERFORMER = "actor performer"
    ACTOR_RECIPIENT = "actor recipient"
    SAME_GATEWAY = "same gateway"
    FURTHER_SPECIFICATION = "further specification"
    FLOW = "flow"
    USES = "uses"
