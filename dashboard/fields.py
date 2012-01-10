from south.modelsinspector import add_introspection_rules
from django.db.models import fields

class PositiveBigIntegerField(fields.BigIntegerField):
    description = "Unsigned auto-increment Big integer"
    MAX_POSITIVE_BIGINT = 18446744073709551615
    
    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': self.MAX_POSITIVE_BIGINT}
        defaults.update(kwargs)
        return super(fields.BigIntegerField, self).formfield(**defaults)
    
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
                return 'bigint(20) UNSIGNED'
        else:
            raise Exception("db not supported")
        
add_introspection_rules([], ["^dashboard\.fields\.PositiveBigIntegerField"])
