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
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the best policies, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getOptimalPolicies():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    team = request.args.get("team", default="Blue", type=str)
    rawState = request.args.get("state", default=0, type=int)
    rawActions = request.args.get("actions", default="bKills", type=str) # comma-delimited string of actions

    actions = rawActions.split(",")
    if len(actions) < 1:
        state = 0
    elif len(actions) == 1:
        state = rawState
    else:
        state = rawState + len(actions) - 1

    optimalPolicy = OptimalPolicy(team)
    bestPolicies = Policies(optimalPolicy.GetOptimalPolicy(state, actions[len(actions) - 1]))
    return PoliciesSchema().dump(bestPolicies), 200

@policy_api.route('/next')
@cross_origin()
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the next actions, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getNextPolicies():
    team = request.args.get("team", default="Blue", type=str)
    state = request.args.get("state", default=0, type=int)
    action = request.args.get("action", default="bKills", type=str)

    optimalPolicy = OptimalPolicy(team)
    nextPolicies = Policies(optimalPolicy.GetNextPolicy(state, action))
    return PoliciesSchema().dump(nextPolicies), 200
    
@policy_api.route('/start')
@cross_origin()
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Returns the next actions, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getStartPolicies():
    team = request.args.get("team", default="Blue", type=str)

    optimalPolicy = OptimalPolicy(team)
    nextPolicies = Policies(optimalPolicy.GetStartPolicy())
    return PoliciesSchema().dump(nextPolicies), 200