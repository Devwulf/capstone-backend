from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from api.model.optimalPolicy import OptimalPolicy
from api.model.policy import Policies
from api.schema.policy import PoliciesSchema

policy_api = Blueprint('policy', __name__)


@policy_api.route('/best')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Retrieves the best policies, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getOptimalPolicy():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    team = request.args.get("team", default="Blue", type=str)
    rawState = request.args.get("state", default=0, type=int)
    rawActions = request.args.get("actions", default="", type=str) # comma-delimited string of actions

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