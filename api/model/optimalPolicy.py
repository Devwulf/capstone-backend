from api.model.dbModels import BlueQValue, Probability, RedQValue
import pandas as pd
import numpy as np
from api.model.policy import Policy

class OptimalPolicy:
    def __init__(self, team) -> None:
        self.team = team
        self.blueDefenses = np.array([4, 4, 4, 2]) # top, mid, bot, and nexus defenses
        self.redDefenses = np.array([4, 4, 4, 2])

    def IsTerminalState(self, startState, startAction):
        if (startAction == "bWon") or (startAction == "rWon") or (startState > 131):
            return True
        return False

    def IsValidStructureAction(self, action):
        if (action == "rTOP_OUTER_TURRET") and (self.blueDefenses[0] != 4):
            return False
        elif (action == "rTOP_INNER_TURRET") and (self.blueDefenses[0] != 3):
            return False
        elif (action == "rTOP_BASE_TURRET") and (self.blueDefenses[0] != 2):
            return False
        elif (action == "rTOP_INHIBITOR") and (self.blueDefenses[0] != 1):
            return False
        elif (action == "rMID_OUTER_TURRET") and (self.blueDefenses[1] != 4):
            return False
        elif (action == "rMID_INNER_TURRET") and (self.blueDefenses[1] != 3):
            return False
        elif (action == "rMID_BASE_TURRET") and (self.blueDefenses[1] != 2):
            return False
        elif (action == "rMID_INHIBITOR") and (self.blueDefenses[1] != 1):
            return False
        elif (action == "rBOT_OUTER_TURRET") and (self.blueDefenses[2] != 4):
            return False
        elif (action == "rBOT_INNER_TURRET") and (self.blueDefenses[2] != 3):
            return False
        elif (action == "rBOT_BASE_TURRET") and (self.blueDefenses[2] != 2):
            return False
        elif (action == "rBOT_INHIBITOR") and (self.blueDefenses[2] != 1):
            return False
        elif (action == "rMID_NEXUS_TURRET") and ((self.blueDefenses[3] <= 0) or ((self.blueDefenses[0] > 0) and (self.blueDefenses[1] > 0) and (self.blueDefenses[2] > 0))):
            #print("rMID_NEXUS_TURRET", "blueDefenses:", blueDefenses)
            return False
        elif (action == "rWon") and (self.blueDefenses[3] > 0):
            #print("rWon", "blueDefenses:", blueDefenses)
            return False

        elif (action == "bTOP_OUTER_TURRET") and (self.redDefenses[0] != 4):
            return False
        elif (action == "bTOP_INNER_TURRET") and (self.redDefenses[0] != 3):
            return False
        elif (action == "bTOP_BASE_TURRET") and (self.redDefenses[0] != 2):
            return False
        elif (action == "bTOP_INHIBITOR") and (self.redDefenses[0] != 1):
            return False
        elif (action == "bMID_OUTER_TURRET") and (self.redDefenses[1] != 4):
            return False
        elif (action == "bMID_INNER_TURRET") and (self.redDefenses[1] != 3):
            return False
        elif (action == "bMID_BASE_TURRET") and (self.redDefenses[1] != 2):
            return False
        elif (action == "bMID_INHIBITOR") and (self.redDefenses[1] != 1):
            return False
        elif (action == "bBOT_OUTER_TURRET") and (self.redDefenses[2] != 4):
            return False
        elif (action == "bBOT_INNER_TURRET") and (self.redDefenses[2] != 3):
            return False
        elif (action == "bBOT_BASE_TURRET") and (self.redDefenses[2] != 2):
            return False
        elif (action == "bBOT_INHIBITOR") and (self.redDefenses[2] != 1):
            return False
        elif (action == "bMID_NEXUS_TURRET") and ((self.redDefenses[3] <= 0) or ((self.redDefenses[0] > 0) and (self.redDefenses[1] > 0) and (self.redDefenses[2] > 0))):
            #print("bMID_NEXUS_TURRET", "redDefenses:", redDefenses)
            return False
        elif (action == "bWon") and (self.redDefenses[3] > 0):
            #print("bWon", "redDefenses:", redDefenses)
            return False
        
        return True

    def UpdateStructures(self, action):
        if not self.IsValidStructureAction(action):
            return
        
        if "rTOP" in action:
            self.blueDefenses[0] = self.blueDefenses[0] - 1
        elif "rMID" in action:
            if "NEXUS" not in action:
                self.blueDefenses[1] = self.blueDefenses[1] - 1
            else:
                self.blueDefenses[3] = self.blueDefenses[3] -  1
        elif "rBOT" in action:
            self.blueDefenses[2] = self.blueDefenses[2] -  1
            
        elif "bTOP" in action:
            self.redDefenses[0] = self.redDefenses[0] - 1
        elif "bMID" in action:
            if "NEXUS" not in action:
                self.redDefenses[1] = self.redDefenses[1] - 1
            else:
                self.redDefenses[3] = self.redDefenses[3] - 1
        elif "bBOT" in action:
            self.redDefenses[2] = self.redDefenses[2] - 1
        
    def GetRows(self, startState, startAction):
        if self.team == "Blue":
            items = BlueQValue.query.filter((BlueQValue.startState == startState) & (BlueQValue.startEvent == startAction)).all()
        else:
            items = RedQValue.query.filter((RedQValue.startState == startState) & (RedQValue.startEvent == startAction)).all()
        return items

    def GetQValue(self, startState, startAction, endAction):
        if self.team == "Blue":
            item = BlueQValue.query.filter((BlueQValue.startState == startState) & (BlueQValue.startEvent == startAction) & (BlueQValue.endEvent == endAction)).first()
        else:
            item = RedQValue.query.filter((RedQValue.startState == startState) & (RedQValue.startEvent == startAction) & (RedQValue.endEvent == endAction)).first()
        return item.qValue if item is not None else 0

    def GetStartProbability(self, startAction):
        item = Probability.query.filter((Probability.startState == -1) & (Probability.startEvent == startAction)).first()
        return item.prob if item is not None else 0

    def GetProbability(self, startState, startAction, endAction):
        item = Probability.query.filter((Probability.startState == startState) & (Probability.startEvent == startAction) & (Probability.endEvent == endAction)).first()
        return item.prob if item is not None else 0

    def GetGoldAdv(self, startState, startAction, endAction):
        item = Probability.query.filter((Probability.startState == startState) & (Probability.startEvent == startAction) & (Probability.endEvent == endAction)).first()
        if item is None:
            choice = np.random.randint(0, 5)
        else:
            probabilities = [item.bAdvFar, item.bAdvClose, item.even, item.rAdvClose, item.rAdvFar]
            if np.sum(probabilities) == 0:
                choice = np.random.randint(0, 5)
            else:
                choice = np.random.choice(5, p=probabilities)
        
        choices = ["bAdvFar", "bAdvClose", "Even", "rAdvClose", "rAdvFar"]
        return choices[choice]

    def GetOptimalPolicy(self, startState, startAction):
        if self.IsTerminalState(startState, startAction):
            return []
        
        optimalPolicy = [Policy(startState, startAction, 1, 0, "Even")]
        currentState = startState
        currentStartAction = startAction
        
        while not self.IsTerminalState(currentState, currentStartAction):
            self.UpdateStructures(currentStartAction)
            availableActions = sorted(self.GetRows(currentState, currentStartAction), key=lambda x: x.qValue, reverse=True)
            nextAction = None
            for row in availableActions:
                if self.IsValidStructureAction(row.endEvent):
                    nextAction = row.endEvent
                    break
            #nextAction = GetNextAction(team, currentState, currentStartAction, 1.)
            if nextAction is None:
                return optimalPolicy
            qValue = self.GetQValue(currentState, currentStartAction, nextAction)
            probability = self.GetProbability(currentState, currentStartAction, nextAction)
            goldAdv = self.GetGoldAdv(currentState, currentStartAction, nextAction)
            currentState += 1
            currentStartAction = nextAction
            optimalPolicy.append(Policy(currentState, nextAction, probability, qValue, goldAdv))
        
        return optimalPolicy

    def GetOptimalPolicyFromActions(self, startState, actions):
        if len(actions) <= 0:
            return []
        elif len(actions) == 1:
            return self.GetOptimalPolicy(startState, actions[0])
        
        optimalPolicy = [Policy(0, actions[0], 1, 0, "Even")]
        for i, action in enumerate(actions[:-1]):
            if (self.IsTerminalState(i, action)) or (not self.IsValidStructureAction(action)):
                return []

            self.UpdateStructures(action)
            nextAction = actions[i + 1]
            qValue = self.GetQValue(i, action, nextAction)
            probability = self.GetProbability(i, action, nextAction)
            goldAdv = self.GetGoldAdv(i, action, nextAction)
            optimalPolicy.append(Policy(i, nextAction, probability, qValue, goldAdv))

        currentState = len(actions) - 1
        currentStartAction = actions[-1]
        
        while not self.IsTerminalState(currentState, currentStartAction):
            self.UpdateStructures(currentStartAction)
            availableActions = sorted(self.GetRows(currentState, currentStartAction), key=lambda x: x.qValue, reverse=True)
            nextAction = None
            for row in availableActions:
                if self.IsValidStructureAction(row.endEvent):
                    nextAction = row.endEvent
                    break
            #nextAction = GetNextAction(team, currentState, currentStartAction, 1.)
            if nextAction is None:
                return optimalPolicy
            qValue = self.GetQValue(currentState, currentStartAction, nextAction)
            probability = self.GetProbability(currentState, currentStartAction, nextAction)
            goldAdv = self.GetGoldAdv(currentState, currentStartAction, nextAction)
            currentState += 1
            currentStartAction = nextAction
            optimalPolicy.append(Policy(currentState, nextAction, probability, qValue, goldAdv))
        
        return optimalPolicy

    def GetNextPolicy(self, startState, startAction):
        if self.IsTerminalState(startState, startAction):
            return []

        nextPolicy = []
        availableActions = self.GetRows(startState, startAction)
        for row in availableActions:
            probability = self.GetProbability(row.startState, row.startEvent, row.endEvent)
            qValue = self.GetQValue(row.startState, row.startEvent, row.endEvent)
            goldAdv = self.GetGoldAdv(row.startState, row.startEvent, row.endEvent)
            policy = Policy(row.startState + 1, row.endEvent, probability, qValue, goldAdv)
            nextPolicy.append(policy)
        
        return nextPolicy

    def GetStartPolicy(self):
        actions = Probability.query.filter(Probability.startState == -1).all()
        policies = []

        for actionObj in actions:
            action = actionObj.endEvent
            if (not self.IsTerminalState(0, action)) and (self.IsValidStructureAction(action)):
                probability = self.GetStartProbability(action)
                policies.append(Policy(0, action, probability, 0, "Even"))

        return policies
