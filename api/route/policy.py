from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.optimalPolicy import OptimalPolicy
from api.model.policy import Policies
from api.schema.policy import PoliciesSchema

policy_api = Blueprint('policy', __name__)


@policy_api.route('/<team>')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Retrieves the best policies, given a starting state and action.',
            'schema': PoliciesSchema
        }
    }
})
def getOptimalPolicy(team):
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    optimalPolicy = OptimalPolicy(team)
    bestPolicies = Policies(optimalPolicy.GetOptimalPolicy(0, "bKills"))
    return PoliciesSchema().dump(bestPolicies), 200