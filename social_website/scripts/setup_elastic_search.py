from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from pyes import ES
from custom_mappings import COMPLETION_MAPPING, FACET_MAPPING, SETTINGS
from indexing_data import enter_data_into_completion_search, enter_data_into_facet_search

def custom_create_index(conn, index_name, settings, mapping):
    try:
        conn.delete_index(index_name)
        print "Previous index deleted for %s" % index_name
    except Exception, ex:
        print "No Previous index for %s" % index_name
    conn.indices.create_index(index_name, settings = settings)
    conn.indices.put_mapping(doc_type = index_name, mapping = mapping, indices = index_name)

facet_index = dg.settings.FACET_INDEX
completion_index = dg.settings.COMPLETION_INDEX
conn = ES(['127.0.0.1:9200'])

# FACET SEARCH   
custom_create_index(conn, facet_index, SETTINGS, FACET_MAPPING)
enter_data_into_facet_search(conn, facet_index)

# COMPLETION SEARCH 
custom_create_index(conn, completion_index, SETTINGS, COMPLETION_MAPPING)
enter_data_into_completion_search(conn, completion_index)



