class Policy:
    def __init__(self, action, probability, qValue, goldAdv) -> None:
        self.action = action
        self.probability = probability
        self.qValue = qValue
        self.goldAdv = goldAdv

class Policies:
    def __init__(self, policies) -> None:
        self.policies = policies