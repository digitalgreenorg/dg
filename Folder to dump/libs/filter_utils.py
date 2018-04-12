import datetime
from django.core.exceptions import FieldError, ValidationError
from django.db.models.query import QuerySet

def filter_objects_for_date(all_objects, date_field_name, search_text):
    """Filters all_objects by matching search_text with a date field.
    
    This function matches dates i.e. "2012-06-30", years i.e. "2012" 
    and months i.e. 06 and filters objects for whom the above matching 
    for the field called date_field_name is successful.
    
    """
    if not isinstance(all_objects, QuerySet):
        return all_objects.none()
    obj_with_date = obj_with_month = obj_with_year = all_objects.none()
    # Filter objects with an exact match with the date
    try: 
        obj_with_date = all_objects.filter(**{date_field_name:search_text})
    except FieldError:
        # TODO Log that some code is calling this function with an incorrect field name
        return all_objects.none()
    except ValidationError:
        pass
    except UnicodeDecodeError:
        pass
    # Filter objects which match the month
    try:
        obj_with_month = all_objects.filter(**{'%s__month' % (date_field_name):search_text})
    except ValueError:
        pass
    # Filter objects which match the year
    try:
        year = int(search_text)
        # Check if this year is within the permissible range
        # If we send a year outside the permissible range we get an error from the SQL database when the query is executed. No exception is thrown here.  
        if year < datetime.MAXYEAR and year > datetime.MINYEAR:
            obj_with_year = all_objects.filter(**{'%s__year' % (date_field_name):year})
    except ValueError:
        pass
    return (obj_with_date | obj_with_month | obj_with_year)

