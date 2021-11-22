class Action:
    def __init__(self):
        self.keyword_triggers = []
        self.hotness_triggered = False

    def __eq__(self, other):
        if not isinstance(other, Action):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.keyword_triggers == other.keyword_triggers and \
               self.hotness_triggered == self.hotness_triggered
