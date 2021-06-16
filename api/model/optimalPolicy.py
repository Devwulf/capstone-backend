import pandas as pd
import numpy as np
from api.model.policy import Policy

class OptimalPolicy:
    def __init__(self, team) -> None:
        if team == "Blue":
            self.team = "Blue"
            self.trainModel = pd.read_pickle("static/blueTrainedwGoldAdv.pkl")
        elif team == "Red":
            self.team = "Red"
            self.trainModel = pd.read_pickle("static/redTrainedwGoldAdv.pkl")
        else:
            print(f"Error: The team '{team}' does not exist.")

        self.mdp = pd.read_pickle("static/mdpDf.pkl")
        self.goldAdvMdp = pd.read_pickle("static/eventsGoldAdvMdp.pkl")
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
                self.redDefenses[3] = self.redDefenses[3]- 1
        elif "bBOT" in action:
            self.redDefenses[2] = self.redDefenses[2] - 1
        
    def GetRows(self, startState, startAction):
        return self.trainModel[(self.trainModel["StartState"] == startState) & (self.trainModel["StartEvent"] == startAction)]

    def GetQValue(self, startState, startAction, endAction):
        return self.trainModel[(self.trainModel["StartState"] == startState) & (self.trainModel["StartEvent"] == startAction) & (self.trainModel["EndEvent"] == endAction)]["QValues"].iloc[0]

    def GetProbability(self, startState, startAction, endAction):
        return self.mdp[(self.mdp["StartState"] == startState) & (self.mdp["StartEvent"] == startAction) & (self.mdp["EndEvent"] == endAction)]["Probability"].iloc[0]

    def GetGoldAdv(self, startState, startAction, endAction):
        row = self.goldAdvMdp[(self.goldAdvMdp["StartState"] == startState) & (self.goldAdvMdp["StartEvent"] == startAction) & (self.goldAdvMdp["EndEvent"] == endAction)]
        probabilities = [row["bAdvFar"].iloc[0], row["bAdvClose"].iloc[0], row["Even"].iloc[0], row["rAdvClose"].iloc[0], row["rAdvFar"].iloc[0]]
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
            availableActions = self.GetRows(currentState, currentStartAction).sort_values("QValues", ascending=False)
            nextAction = None
            for row in availableActions.itertuples():
                if self.IsValidStructureAction(row.EndEvent):
                    nextAction = row.EndEvent
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