'''
    how to use marshmallow
'''

from marshmallow import Schema, fields, pprint, ValidationError
import datetime as dt

class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.created_at = dt.datetime.now()

def validate_password(pwd):
    if len(pwd) < 6 or len(pwd) > 12:
        raise ValidationError('length of the password should between 6 and 12 chars')

class UserSchema(Schema):
    name = fields.Str()
    fullname = fields.Str()
    password = fields.Str(validate=validate_password)
    created_at = fields.DateTime()

'''
class UserSchema(Schema):
    name = fields.Str()
    fullname = fields.Str()
    password = fields.Str()
    created_at = fields.DateTime()

    @validates('password')
    def validate_password(self, pwd):
        if len(pwd) < 6 or len(pwd) > 12:
            raise ValidationError('length of the password should between 6 and 12 chars')
'''


wilber = User(name='Wilber', fullname='Wilber Tian', password='wt_password')
schema = UserSchema()
result = schema.dump(wilber)
pprint(result.data)


will = {
    'created_at': '2014-08-11T05:26:03.869245',
    'password': u'wt_password',
    'fullname': u'Will Tian',
    'name': u'Will'
}

result = schema.load(will)
pprint(result.data)


will_error = {
    'created_at': '2014-08-11T05:26:03.869245',
    'password': u'wt_password________',
    'fullname': u'Will Tian',
    'name': u'Will'
}

result, errors = schema.load(will_error)
pprint(errors)