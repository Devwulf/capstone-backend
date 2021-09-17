from flask_marshmallow import Schema
from marshmallow import fields

class TwoDPointSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["x", "y"]

    x = fields.Float()
    y = fields.Float()

class TwoDGraphSchema(Schema):
    class Meta:
        fields = ["points"]

    points = fields.Nested(TwoDPointSchema, many=True)

class LabeledPointSchema(Schema):
    class Meta:
        fields = ["label", "value"]
    
    label = fields.Str()
    value = fields.Float()

class LabeledGraphSchema(Schema):
    class Meta:
        fields = ["points"]

    points = fields.Nested(LabeledPointSchema, many=True)