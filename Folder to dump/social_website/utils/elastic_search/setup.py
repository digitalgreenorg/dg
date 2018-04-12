from pyes import ES

import dg.settings

from custom_mappings import COMPLETION_MAPPING, FACET_MAPPING, SETTINGS, VIDEO_MAPPING
from index import enter_data_into_completion_search, enter_data_into_facet_search, enter_data_into_video_search

def custom_create_index(conn, index_name, settings, mapping):
    try:
        conn.delete_index(index_name)
        print "Previous index deleted for %s" % index_name
    except Exception, ex:
        print "No Previous index for %s" % index_name
    conn.indices.create_index(index_name, settings = settings)
    conn.indices.put_mapping(doc_type = index_name, mapping = mapping, indices = index_name)


def setup_elastic_search():
    facet_index = dg.settings.FACET_INDEX
    completion_index = dg.settings.COMPLETION_INDEX
    video_index = dg.settings.VIDEO_INDEX
    conn = ES(['127.0.0.1:9200'])

    # FACET SEARCH   
    custom_create_index(conn, facet_index, SETTINGS, FACET_MAPPING)
    enter_data_into_facet_search(conn, facet_index)

    # COMPLETION SEARCH 
    custom_create_index(conn, completion_index, SETTINGS, COMPLETION_MAPPING)
    enter_data_into_completion_search(conn, completion_index)

    # VIDEO SEARCH
    custom_create_index(conn, video_index, SETTINGS, VIDEO_MAPPING)
    enter_data_into_video_search(conn, video_index)