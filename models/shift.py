import datetime as dt

from marshmallow import Schema, fields
from marshmallow import post_load

class Shift(object):
    def __init__(self, date_start, date_end, process, parameters, userId):
        self.date_start = date_start
        self.date_end = date_end
        self.process = process
        self.parameters = parameters
        self.userId = userId


class ShiftSchema(Schema):
    date_start = fields.Str()
    date_end = fields.Str()
    process = fields.Str()
    parameters = fields.Str()
    userId = fields.Str()

    @post_load
    def make_shift(self, data, **kwargs):
        return Shift(**data)
    
