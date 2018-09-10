from django.core.management.base import BaseCommand
from django.contrib.auth.models import *
from django.db.models.manager import *
from django.db import models
from activities.models import *
from geographies.models import *
from videos.models import *
from training.models import *
from people.models import *
from training.models import *
from coco.models import *
from ap_migration_config import *
from django.apps import apps
from django.db import connection
import logging

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.info('Querying the mapping table')
        mapping_queryset = AP_COCO_Mapping.objects.values('id','geo_type','ap_geo_id','coco_geo_id')
        logger.info('Query Completed')
        logger.info('Number of rows - %s' % (str(mapping_queryset.count())))
        logger.info('Iterating the queryset')
        for item in mapping_queryset:
            try:
                geo_type = item.get('geo_type')
                ap_geo_id = item.get('ap_geo_id')
                coco_geo_id = item.get('coco_geo_id')
                obj = migration_config.get(geo_type)
                logger.info('Migrating foreign key dependent models for geography type - %s, Old Id - %s, New Id - %s' % (geo_type, ap_geo_id, coco_geo_id))
                for foreign_key_model in obj.get('foreign_key_models'):
                    try:
                        logger.info('Updating foreign key model - %s for app - %s' % (foreign_key_model.get('model'),foreign_key_model.get('app_label')))
                        model = apps.get_model(foreign_key_model.get('app_label'), foreign_key_model.get('model'))
                        filter_kwargs , update_kwargs = {}, {}
                        filter_kwargs[obj.get('field')] = ap_geo_id
                        update_kwargs[obj.get('field')] = coco_geo_id
                        result = model.objects.filter(**filter_kwargs).update(**update_kwargs)
                        logger.info('Number of objects updated - %s' % (result))
                    except Exception as e:
                        logger.error('Error updating foreign key model - %s for app - %s' % (foreign_key_model.get('model'),foreign_key_model.get('app_label')))
                        logger.error(e)
                logger.info('Foreign Key dependent models updated successfully')
                    
                if obj.get('m2m_models'):
                    logger.info('Migrating m2m dependent tables for geography type - %s, Old Id - %s, New Id - %s' % (geo_type, ap_geo_id, coco_geo_id))
                    for m2m_model in obj.get('m2m_models'):
                        try:
                            logger.info('Migrating m2m table - %s' % (m2m_model.get('m2m_table')))
                            with connection.cursor() as cursor:
                                query = '''select %s_id, group_concat(distinct %s separator ',') from %s where %s in (%s,%s) group by %s_id''' % (m2m_model.get('model'), obj.get('field'), m2m_model.get('m2m_table'), obj.get('field'), ap_geo_id, coco_geo_id, m2m_model.get('model'))
                                logger.info('query for retrieving rows that have both ids')
                                logger.info(query)
                                cursor.execute(query)
                                for row in list(cursor.fetchall()):
                                    m2m_field_list = row[1].split(',')
                                    if len(m2m_field_list) > 1:
                                        for field_id in m2m_field_list:
                                            if field_id == str(ap_geo_id):
                                                delete_query = '''delete from %s where %s_id=%s and %s=%s''' % \
                                                            (m2m_model.get('m2m_table'), m2m_model.get('model'), str(row[0]), obj.get('field'), field_id)
                                                logger.info('For case when both ids are already assigned to a single %s_id, we need to delete the old id to avoid integrity conflict' % (m2m_model.get('model')))
                                                logger.info(delete_query)
                                                cursor.execute(delete_query)
                                    else:
                                        if m2m_field_list[0] == str(ap_geo_id):
                                            update_query = '''update %s set %s=%s where %s_id=%s and %s=%s''' % \
                                                            (m2m_model.get('m2m_table'), obj.get('field'), coco_geo_id, m2m_model.get('model'), str(row[0]), obj.get('field'), str(ap_geo_id))
                                            logger.info('Updating the old id as usual')
                                            logger.info(update_query)
                                            cursor.execute(update_query)
                            logger.info('m2m table - %s updated successfully' % (m2m_model.get('m2m_table')))
                        except Exception as e:
                            logger.error('Error updating m2m table - %s' % (m2m_model.get('m2m_table')))
                            logger.error(e)
                
                    logger.info('All m2m tables updated successfully')
                logger.info('Updating active status of geo type - %s with id - %s' % (geo_type, ap_geo_id))
                geo_model = apps.get_model('geographies', geo_type)
                geo_model.objects.filter(id=ap_geo_id).update(active=False)
                logger.info('Active status changed to False')
            except Exception as e:
                logger.error('Some unknown error is encountered')
                logger.error(e)


                