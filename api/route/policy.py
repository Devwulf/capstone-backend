from api.model.graphs import TwoDGraph
from api.schema.graphs import LabeledGraphSchema, TwoDGraphSchema
from auth.utils.decorators import token_required
from http import HTTPStatus
from flask import Blueprint, request
from flask_cors import cross_origin
from flasgger import swag_from
from api.model.optimalPolicy import OptimalPolicy
from api.model.policy import Policies
from api.schema.policy import PoliciesSchema

policy_api = Blueprint('policy', __name__)


@policy_api.route('/best')
@cross_origin()
@token_required
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the best policies, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getOptimalPolicies(currentUser):
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    team = request.args.get("team", default="Blue", type=str)
    rawState = request.args.get("state", default=0, type=int)
    rawActions = request.args.get("actions", default="bKills", type=str) # comma-delimited string of actions

    actions = rawActions.split(",")
    state = rawState
    if len(actions) < 1:
        state = 0

    optimalPolicy = OptimalPolicy(team)
    bestPolicies = Policies(optimalPolicy.GetOptimalPolicyFromActions(state, actions))
    return PoliciesSchema().dump(bestPolicies), 200

@policy_api.route('/next')
@cross_origin()
@token_required
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the next actions, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getNextPolicies(currentUser):
    team = request.args.get("team", default="Blue", type=str)
    state = request.args.get("state", default=0, type=int)
    action = request.args.get("action", default="bKills", type=str)

    optimalPolicy = OptimalPolicy(team)
    nextPolicies = Policies(optimalPolicy.GetNextPolicy(state, action))
    return PoliciesSchema().dump(nextPolicies), 200
    
@policy_api.route('/start')
@cross_origin()
@token_required
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the next actions, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getStartPolicies(currentUser):
    team = request.args.get("team", default="Blue", type=str)

    optimalPolicy = OptimalPolicy(team)
    nextPolicies = Policies(optimalPolicy.GetStartPolicy())
    return PoliciesSchema().dump(nextPolicies), 200

@policy_api.route('/line')
@cross_origin()
@token_required
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the preprocessed data representing a line graph, given an end action and if the probability graph is wanted',
            'schema': TwoDGraphSchema
        }
    }
})
def getLineGraph(currentUser):
    team = request.args.get("team", default="Blue", type=str)
    endAction = request.args.get("endAction", default="bKills", type=str)
    isProbability = request.args.get("isProbability", default=True, type=bool)

    optimalPolicy = OptimalPolicy(team)
    graph = optimalPolicy.GetLineGraph(endAction, isProbability)
    return TwoDGraphSchema().dump(graph), 200

@policy_api.route('/pie')
@cross_origin()
@token_required
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the preprocessed data representing a pie chart, given a start state, start action, and if kills should be included',
            'schema': LabeledGraphSchema
        }
    }
})
def getPieChart(currentUser):
    team = request.args.get("team", default="Blue", type=str)
    startState = request.args.get("startState", default=0, type=int)
    startAction = request.args.get("startAction", default="bKills", type=str)
    hasKills = request.args.get("hasKills", default=True, type=bool)

    optimalPolicy = OptimalPolicy(team)
    graph = optimalPolicy.GetPieChart(startState, startAction, hasKills)
    return LabeledGraphSchema().dump(graph), 200