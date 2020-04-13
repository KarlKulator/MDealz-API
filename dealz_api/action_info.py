class ActionInfo:
    def __init__(self):
        self.keyword_triggers = []

    def __eq__(self, other):
        if not isinstance(other, ActionInfo):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.keyword_triggers == other.keyword_triggers

