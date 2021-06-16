from flask_marshmallow import Schema
from marshmallow import fields

class PolicySchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["action", "probability", "qValue", "goldAdv"]

    action = fields.Str()
    probability = fields.Float()
    qValue = fields.Float()
    goldAdv = fields.Str()

class PoliciesSchema(Schema):
    class Meta:
        fields = ["policies"]

    policies = fields.Nested(PolicySchema, many=True)