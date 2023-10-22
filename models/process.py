import datetime as dt

from marshmallow import Schema, fields
from marshmallow import post_load

class Process(object):
    def __init__(self, name, area):
        self.name = name
        self.area = area


class ProcessSchema(Schema):
    name = fields.Str()
    area = fields.Str()
    
    @post_load
    def make_process(self, data, **kwargs):
        return Process(**data)