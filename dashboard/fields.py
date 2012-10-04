from django.core.exceptions import ValidationError
from django.db.models import fields
from south.modelsinspector import add_introspection_rules

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
        
class BigAutoField(fields.AutoField):
        
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

class BigForeignKey(fields.related.ForeignKey):

    def db_type(self, connection):
        rel_field = self.rel.get_related_field()
        # next lines are the "bad tooth" in the original code:
        if (isinstance(rel_field, BigAutoField) or
                (not connection.features.related_fields_match_type and
                isinstance(rel_field, PositiveBigIntegerField))):
            # because it continues here in the django code:
            # return PositiveBigIntegerField().db_type()
            # thereby fixing any BigAutoField as PositiveBigIntegerField
            return PositiveBigIntegerField().db_type(connection=connection)
        return rel_field.db_type()

add_introspection_rules([], ["^dashboard\.fields\.PositiveBigIntegerField"])
add_introspection_rules([], ["^dashboard\.fields\.BigAutoField"])
add_introspection_rules([], ["^dashboard\.fields\.BigForeignKey"])

