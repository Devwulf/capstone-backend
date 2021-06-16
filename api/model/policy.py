class Policy:
    def __init__(self, state, action, probability, qValue, goldAdv) -> None:
        self.state = state
        self.action = action
        self.probability = probability
        self.qValue = qValue
        self.goldAdv = goldAdv

class Policies:
    def __init__(self, policies) -> None:
        self.policies = policies