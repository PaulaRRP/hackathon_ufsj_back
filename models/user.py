import datetime as dt

from marshmallow import Schema, fields
from marshmallow import post_load

class User(object):
    def __init__(self, name, email, password, register, job, area, contact):
        self.name = name
        self.email = email
        self.password = password
        self.register = register
        self.job = job
        self.area = area
        self.contact = contact


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    register = fields.Str()
    job = fields.Str()
    area = fields.Str()
    contact = fields.Str()

    @post_load
    def make_User(self, data, **kwargs):
        return User(**data)
    
       