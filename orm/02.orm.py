class Field(object):
    def __init__(self, fname, ftype):
        self.fname = fname
        self.ftype = ftype

class StringField(Field):
    def __init__(self, fname, ftype='varchar(50)'):
        super(StringField, self).__init__(fname, ftype)

class IntegerField(Field):
    def __init__(self, fname, ftype='int'):
        super(IntegerField, self).__init__(fname, ftype)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)
        else:
            mapping = {}
            print "Create Model for:", name
            for k, v in attrs.items():
                if isinstance(v, Field):
                    print "mapping %s with %s" %(k, v)
                    mapping[k] = v
            attrs['_table'] = name 
            attrs['_mapping'] = mapping 
            return type.__new__(cls, name, bases, attrs)     

class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.__class__._mapping.keys():
                print "Key '%s' is not defined for %s" %(key, self.__class__.__name__)
                return 
        super(Model, self).__init__(**kwargs)

    def save(self):
        fields = []
        params = []
        for k, v in self.__class__._mapping.items():
            fields.append(k)
            params.append("'{0}'".format(self[k]))
        sql = 'insert into %s (%s) values (%s)' % (self.__class__._table, ','.join(fields), ','.join(params))
        print 'SQL: %s' %sql 


class Student(Model):
    id = IntegerField('id_column')
    name = StringField('username_column')
    email = StringField('email_column')
    
print "-------------------------------------------------"
print Student._table
print Student._mapping
print "-------------------------------------------------"
s1 = Student(id = 1, name = "Wilber", email = "wilber@sh.com")    
s1.save()
print "-------------------------------------------------"
s2 = Student(id = 1, name = "Wilber", gender = "male")   
        
