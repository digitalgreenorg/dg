from django.core.exceptions import ValidationError
from django.db.models.fields import AutoField, BigIntegerField
from south.modelsinspector import add_introspection_rules

class PositiveBigIntegerField(BigIntegerField):
    description = "Unsigned auto-increment Big integer"
    MAX_POSITIVE_BIGINT = 18446744073709551615
    
    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': self.MAX_POSITIVE_BIGINT}
        defaults.update(kwargs)
        return super(BigIntegerField, self).formfield(**defaults)
    
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
                return 'bigint(20) UNSIGNED'
        else:
            raise Exception("db not supported")
        
class BigAutoField(AutoField):
        
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "bigint(20) UNSIGNED AUTO_INCREMENT"
        else:
            pass
    
    def get_internal_type(self):
        return "BigAutoField"
    
    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise ValidationError(
                _("This value must be a long integer."))


add_introspection_rules([], ["^dashboard\.fields\.fields\.PositiveBigIntegerField"])
add_introspection_rules([], ["^dashboard\.fields\.fields\.BigAutoField"])

