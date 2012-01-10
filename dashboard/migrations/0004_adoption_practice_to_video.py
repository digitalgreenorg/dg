# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        import sys, os, datetime, traceback
        from collections import defaultdict
        
        class Obj():
             pass
        
        paps = orm.PersonAdoptPractice.objects.all()
        pmas = orm.PersonMeetingAttendance.objects.filter(person__in = paps.values('person')).values('person', 'screening__date', 'screening__videoes_screened', 'screening__videoes_screened__related_agricultural_practices')
        
        #For all the pma data, create a ds
        #dict of per_id to list of pma obj,
        per_data = {}
        for pma in pmas:
            obj = Obj()
            obj.date = pma['screening__date']
            obj.vid = pma['screening__videoes_screened']
            obj.pr = pma['screening__videoes_screened__related_agricultural_practices']
            pid = pma['person']
            if pid in per_data:
                per_data[pid].append(obj)
            else:
                per_data[pid] = [obj]
        
        #sort the list for each person based on screening date in descending order
        for ls in per_data.itervalues():
            ls.sort(cmp = lambda x, y: cmp(x.date, y.date), reverse=True)
        
        print "Finished creating per_data ds"
        
        paps = list(paps.order_by('-date_of_adoption'))
        vid_ado = [] #This will have tuples of adoption and pma object which matched (screening date was earlier and practice was same. latest will be matched)
        err_ado = [] #adoption of persons who haven't seen a screening at all or that didn't match with screenings
        
        for pap in paps:
            if pap.person.id not in per_data:
                err_ado.append(pap)
                continue
            ls = per_data[pap.person.id]
            found = False
            for obj in ls:
                if obj.date > pap.date_of_adoption:
                    continue
                elif (pap.practice.id == obj.pr and (obj.date - pap.date_of_adoption).days <= 180 ):
                    ls.remove(obj)
                    pap.video = orm.Video.objects.get(id = obj.vid)
                    pap.save()
                    vid_ado.append((pap, obj))
                    found = True
                    break
            if(not found):
                err_ado.append(pap)
        
        print "Finished current matching: matched=", len(vid_ado), "\n\terrors = ", len(err_ado)        
        
        ## END OF CURRENT MATCHING ##
        ## STARTING ERROR SHEET PARSING ##
        
        new_vid_ado = []
        def verify_and_save_correction(ado):
            if ado.person.id not in per_data:
                return False
            ls = per_data[ado.person.id]
            for obj in ls:
                if obj.date > ado.date_of_adoption:
                    continue
                elif (ado.practice.id == obj.pr and (obj.date - ado.date_of_adoption).days <= 180):
                    ls.remove(obj)
                    ado.video = orm.Video.objects.get(id = obj.vid)
                    ado.save()
                    new_vid_ado.append((ado, obj))
                    return True
            return False
        
        paps = list(orm.PersonAdoptPractice.objects.select_related(depth=1).all())
        papd = defaultdict(list)
        for pap in paps:
            papd[pap.person.id].append(pap)
        
        for papl in papd.values():
            papl.sort(cmp = lambda x, y: cmp(x.date_of_adoption, y.date_of_adoption))
            
        print "Finished structuring data for Adoption"
        
        def match_excel_with_db(ado_tuple, per_id):
            for ado in papd[per_id]:
                if ado.date_of_adoption < ado_tuple[0]:
                    continue
                if ado.date_of_adoption == ado_tuple[0]:
                    if ado_tuple[1] == ado.practice.practice_name:
                        return ado
                if ado.date_of_adoption > ado_tuple[0]:
                    break
            return None
            
        def search_in_err_ado(pap_db_obj):
            for ado in err_ado:
                if pap_db_obj.id == ado.id:
                    return ado
            return None
            
        pracs = list(orm.Practices.objects.all())
        pracd = dict()
        for prac in pracs:
            pracd[prac.practice_name.lower()] = prac
        
        print "Finished structuring practices"
        
        file_path = os.path.dirname(os.path.abspath(__file__))
        file_names_dir = [os.path.join(file_path, r"adoption_correction_csvs/Dharwad_1_23_12.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Dharwad_2_23_12.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Mysore.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Hassan.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Belguam_combined.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/corrected Adoption eror UJJAIN 21 07 2011.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/DG error Correction Barwani 210911 (1).csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Dindori .csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Jhabua Dg (1).csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Narsinghpur DG Error (2).csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Ratlam D.G.Adoption Error.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Rajgarh.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Pradan_karanjia.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Pradan_khunti.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Pradan_westsinghbhum.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Pragati_koraput.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Pragati_nandpur.csv"),
        os.path.join(file_path, r"adoption_correction_csvs/Varrat_keonjhar.csv")
        ]
        unmatched = list()
        not_error_now = list()
        pr_not_match = list()
        invalid_correction = list()
        to_delete = list()
        for file_name in file_names_dir:
            f = open(file_name)
            lines = f.readlines()
            try:
                for line in lines[1:]:
                    line = line.split(';')
                    if line[0] != "":
                        cur_id = int(line[0])
                    if line[4] != "" and line[6] == "":
                        raise Exception("date present, no practice" + str(line))
                    if line[4] == "" and line[6] != "":
                        raise Exception("date absent, practice present" + str(line))
                    if line[4] != "" and line[6] != "":
                        excel_ado = [datetime.date(*(map(int,line[4].split('-')))), line[6]]
                        db_ado = match_excel_with_db(excel_ado, cur_id)
                        if db_ado == None:
                            unmatched.append((cur_id, excel_ado))
                            continue
                        err_ado_entry = search_in_err_ado(db_ado)
                        if err_ado_entry == None:
                            not_error_now.append(db_ado)
                            continue
                        if line[5] == line[4]:
                            line[5] = ""
                        if line[7] == line[6]:
                            line[7] = ""
                        if line[5] == "" and line[7] == "":
                            to_delete.append(db_ado)
                            err_ado.remove(err_ado_entry)
                            db_ado.delete()
                            continue
                        elif line[5] != "":
                            db_ado.date_of_adoption = datetime.date(*(map(int,line[5].split('-'))))
                        elif line[7] != "":
                            if line[7].lower() not in pracd:
                                pr_not_match.append(excel_ado)
                                continue
                            db_ado.practice = pracd[line[7].lower()]
                        if(not verify_and_save_correction(db_ado)):
                            invalid_correction.append(excel_ado)
                        else:
                            err_ado.remove(err_ado_entry)
            except Exception, e:
                traceback.print_exc()
                print e,"\n", line, "\n", file_name
                exit()
            f.close()
            print "Processed " + file_name
        
        print "Further corrected:", len(new_vid_ado)
        print "Deleted as marked by field officers:", len(to_delete)
        print "Still remaining:", len(err_ado)
        
        del_count = 0
        date_aprox = []
        def err_ado_cmp(x, y):
            if x.person.id == y.person.id:
                return cmp(x.date_of_adoption, y.date_of_adoption)
            else:
                return cmp(x.person.id, y.person.id)
        #sort by person, date_of_adoption in descending
        err_ado.sort(cmp = err_ado_cmp, reverse=True)
        for ado in err_ado:
            if ado.person.id not in per_data:
                del_count = del_count + 1
                ado.delete()
                continue
            else:
                found = False
                ls = per_data[ado.person.id]
                for obj in ls:
                    if ado.practice.id == obj.pr and (obj.date - ado.date_of_adoption).days <= 30:
                        ls.remove(obj)
                        ado.date_of_adoption = obj.date + datetime.timedelta(days = 1)
                        ado.video = orm.Video.objects.get(id = obj.vid)
                        ado.save()
                        date_aprox.append((ado, obj))
                        found = True
                        break
                if not found:
                    del_count = del_count + 1
                    ado.delete()
        print "Final deleted:", del_count
        print "date approximations:", len(date_aprox)

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.animator': {
            'Meta': {'unique_together': "(('name', 'gender', 'partner', 'village'),)", 'object_name': 'Animator', 'db_table': "u'ANIMATOR'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'assigned_villages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assigned_villages'", 'to': "orm['dashboard.Village']", 'through': "orm['dashboard.AnimatorAssignedVillage']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'camera_operator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CAMERA_OPERATOR_FLAG'", 'blank': 'True'}),
            'csp_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CSP_FLAG'", 'blank': 'True'}),
            'facilitator_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'FACILITATOR_FLAG'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'db_column': "'home_village_id'"})
        },
        'dashboard.animatorassignedvillage': {
            'Meta': {'object_name': 'AnimatorAssignedVillage', 'db_table': "u'ANIMATOR_ASSIGNED_VILLAGE'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.animatorsalarypermonth': {
            'Meta': {'object_name': 'AnimatorSalaryPerMonth', 'db_table': "u'ANIMATOR_SALARY_PER_MONTH'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'pay_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PAY_DATE'", 'blank': 'True'}),
            'total_salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_SALARY'", 'blank': 'True'})
        },
        'dashboard.block': {
            'Meta': {'object_name': 'Block', 'db_table': "u'BLOCK'"},
            'block_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'BLOCK_NAME'"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.developmentmanager': {
            'Meta': {'object_name': 'DevelopmentManager', 'db_table': "u'DEVELOPMENT_MANAGER'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'}),
            'speciality': ('django.db.models.fields.TextField', [], {'db_column': "'SPECIALITY'", 'blank': 'True'}),
            'start_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DAY'", 'blank': 'True'})
        },
        'dashboard.district': {
            'Meta': {'object_name': 'District', 'db_table': "u'DISTRICT'"},
            'district_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'DISTRICT_NAME'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']"}),
            'fieldofficer_startday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'FIELDOFFICER_STARTDAY'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Partners']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.State']"})
        },
        'dashboard.equipment': {
            'Meta': {'object_name': 'Equipment', 'db_table': "u'EQUIPMENT_ID'"},
            'additional_accessories': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COST'", 'blank': 'True'}),
            'equipment_type': ('django.db.models.fields.IntegerField', [], {'db_column': "'EQUIPMENT_TYPE'"}),
            'equipmentholder': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.EquipmentHolder']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'installation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'INVOICE_NO'"}),
            'is_reserve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'MODEL_NO'", 'blank': 'True'}),
            'other_equipment': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'db_column': "'OTHER_EQUIPMENT'", 'blank': 'True'}),
            'procurement_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'PROCUREMENT_DATE'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'purpose'", 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'SERIAL_NO'", 'blank': 'True'}),
            'transfer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']", 'null': 'True', 'blank': 'True'}),
            'warranty_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'WARRANTY_EXPIRATION_DATE'", 'blank': 'True'})
        },
        'dashboard.equipmentholder': {
            'Meta': {'object_name': 'EquipmentHolder', 'db_table': "u'EQUIPMENT_HOLDER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.error': {
            'Meta': {'unique_together': "(('rule', 'content_type1', 'object_id1', 'content_type2', 'object_id2'),)", 'object_name': 'Error'},
            'content_type1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type1'", 'to': "orm['contenttypes.ContentType']"}),
            'content_type2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type2'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notanerror': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id1': ('dashboard.fields.PositiveBigIntegerField', [], {}),
            'object_id2': ('dashboard.fields.PositiveBigIntegerField', [], {'null': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dashboard.Rule']"})
        },
        'dashboard.fieldofficer': {
            'Meta': {'object_name': 'FieldOfficer', 'db_table': "u'FIELD_OFFICER'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'HIRE_DATE'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'salary': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'SALARY'", 'blank': 'True'})
        },
        'dashboard.groupstargetedinscreening': {
            'Meta': {'object_name': 'GroupsTargetedInScreening', 'db_table': "u'SCREENING_farmer_groups_targeted'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'persongroups': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'db_column': "'persongroups_id'"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"})
        },
        'dashboard.language': {
            'Meta': {'object_name': 'Language', 'db_table': "u'LANGUAGE'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100'})
        },
        'dashboard.monthlycostpervillage': {
            'Meta': {'object_name': 'MonthlyCostPerVillage', 'db_table': "u'MONTHLY_COST_PER_VILLAGE'"},
            'community_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'COMMUNITY_COST'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'digitalgreen_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'DIGITALGREEN_COST'", 'blank': 'True'}),
            'equipment_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'EQUIPMENT_COST'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'labor_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LABOR_COST'", 'blank': 'True'}),
            'miscellaneous_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'MISCELLANEOUS_COST'", 'blank': 'True'}),
            'partners_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'PARTNERS_COST'", 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TOTAL_COST'", 'blank': 'True'}),
            'transportation_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'TRANSPORTATION_COST'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.partners': {
            'Meta': {'object_name': 'Partners', 'db_table': "u'PARTNERS'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'date_of_association': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'DATE_OF_ASSOCIATION'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'partner_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PARTNER_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'})
        },
        'dashboard.person': {
            'Meta': {'unique_together': "(('person_name', 'father_name', 'group', 'village'),)", 'object_name': 'Person', 'db_table': "u'PERSON'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'ADDRESS'", 'blank': 'True'}),
            'adopted_agricultural_practices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Practices']", 'null': 'True', 'through': "orm['dashboard.PersonAdoptPractice']", 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'db_column': "'AGE'", 'blank': 'True'}),
            'date_of_joining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'FATHER_NAME'", 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'GENDER'"}),
            'group': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.PersonGroups']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'land_holdings': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'LAND_HOLDINGS'", 'blank': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PERSON_NAME'"}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'PHONE_NO'", 'blank': 'True'}),
            'relations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rel'", 'to': "orm['dashboard.Person']", 'through': "orm['dashboard.PersonRelations']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personadoptpractice': {
            'Meta': {'unique_together': "(('person', 'practice', 'date_of_adoption'),)", 'object_name': 'PersonAdoptPractice', 'db_table': "u'PERSON_ADOPT_PRACTICE'"},
            'date_of_adoption': ('django.db.models.fields.DateField', [], {'db_column': "'DATE_OF_ADOPTION'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'practice': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'null': 'True', 'blank': 'True'}),
            'prior_adoption_flag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'PRIOR_ADOPTION_FLAG'", 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'QUALITY'", 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'QUANTITY'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_column': "'QUANTITY_UNIT'", 'blank': 'True'}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']"})
        },
        'dashboard.persongroups': {
            'Meta': {'unique_together': "(('group_name', 'village'),)", 'object_name': 'PersonGroups', 'db_table': "u'PERSON_GROUPS'"},
            'days': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'DAYS'", 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'GROUP_NAME'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'TIME_UPDATED'", 'blank': 'True'}),
            'timings': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'TIMINGS'", 'blank': 'True'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.personmeetingattendance': {
            'Meta': {'object_name': 'PersonMeetingAttendance', 'db_table': "u'PERSON_MEETING_ATTENDANCE'"},
            'expressed_adoption': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_ADOPTION'", 'blank': 'True'}),
            'expressed_adoption_practice': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_adoption_practice'", 'null': 'True', 'to': "orm['dashboard.Practices']"}),
            'expressed_interest': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_INTEREST'", 'blank': 'True'}),
            'expressed_interest_practice': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_interest_practice'", 'null': 'True', 'to': "orm['dashboard.Practices']"}),
            'expressed_question': ('django.db.models.fields.CharField', [], {'max_length': '500', 'db_column': "'EXPRESSED_QUESTION'", 'blank': 'True'}),
            'expressed_question_practice': ('dashboard.fields.BigForeignKey', [], {'blank': 'True', 'related_name': "'expressed_question_practice'", 'null': 'True', 'to': "orm['dashboard.Practices']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']"}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']"})
        },
        'dashboard.personrelations': {
            'Meta': {'object_name': 'PersonRelations', 'db_table': "u'PERSON_RELATIONS'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'related_name': "'person'", 'to': "orm['dashboard.Person']"}),
            'relative': ('dashboard.fields.BigForeignKey', [], {'related_name': "'relative'", 'to': "orm['dashboard.Person']"}),
            'type_of_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'TYPE_OF_RELATIONSHIP'"})
        },
        'dashboard.personshowninvideo': {
            'Meta': {'object_name': 'PersonShownInVideo', 'db_table': "u'VIDEO_farmers_shown'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'person': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Person']", 'db_column': "'person_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.practices': {
            'Meta': {'object_name': 'Practices', 'db_table': "u'PRACTICES'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '200', 'db_column': "'PRACTICE_NAME'"}),
            'seasonality': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_column': "'SEASONALITY'"}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'})
        },
        'dashboard.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'REGION'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.regiontest': {
            'Meta': {'object_name': 'RegionTest', 'db_table': "u'REGION_TEST'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'region_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'REGION_NAME'"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'})
        },
        'dashboard.reviewer': {
            'Meta': {'object_name': 'Reviewer', 'db_table': "u'REVIEWER'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'object_id': ('dashboard.fields.PositiveBigIntegerField', [], {})
        },
        'dashboard.rule': {
            'Meta': {'object_name': 'Rule'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error_msg': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dashboard.screening': {
            'Meta': {'unique_together': "(('date', 'start_time', 'end_time', 'location', 'village'),)", 'object_name': 'Screening', 'db_table': "u'SCREENING'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'DATE'"}),
            'end_time': ('django.db.models.fields.TimeField', [], {'db_column': "'END_TIME'"}),
            'farmer_groups_targeted': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.PersonGroups']", 'symmetrical': 'False'}),
            'farmers_attendance': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dashboard.Person']", 'null': "'False'", 'through': "orm['dashboard.PersonMeetingAttendance']", 'blank': "'False'"}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'LOCATION'", 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'db_column': "'START_TIME'"}),
            'target_adoptions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_ADOPTIONS'", 'blank': 'True'}),
            'target_audience_interest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_AUDIENCE_INTEREST'", 'blank': 'True'}),
            'target_person_attendance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'TARGET_PERSON_ATTENDANCE'", 'blank': 'True'}),
            'videoes_screened': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Video']", 'symmetrical': 'False'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.state': {
            'Meta': {'object_name': 'State', 'db_table': "u'STATE'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'region': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'state_name': ('django.db.models.fields.CharField', [], {'unique': "'True'", 'max_length': '100', 'db_column': "'STATE_NAME'"})
        },
        'dashboard.target': {
            'Meta': {'unique_together': "(('district', 'month_year'),)", 'object_name': 'Target'},
            'adoption_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avg_attendance_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'challenges': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'clusters_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'crp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_identification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'csp_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dg_concept_sharing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dissemination_set_deployment': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'disseminations': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']"}),
            'editor_refresher_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'editor_training': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exp_interest_per_dissemination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'month_year': ('django.db.models.fields.DateField', [], {}),
            'storyboard_preparation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'support_requested': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video_editing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_production': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_quality_checking': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_shooting': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video_uploading': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'village_operationalization': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'villages_certification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'what_not_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'what_went_well': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'dashboard.training': {
            'Meta': {'unique_together': "(('training_start_date', 'training_end_date', 'village'),)", 'object_name': 'Training', 'db_table': "u'TRAINING'"},
            'animators_trained': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Animator']", 'symmetrical': 'False'}),
            'development_manager_present': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.DevelopmentManager']", 'null': 'True', 'db_column': "'dm_id'", 'blank': 'True'}),
            'fieldofficer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.FieldOfficer']", 'db_column': "'fieldofficer_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_END_DATE'"}),
            'training_outcome': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_OUTCOME'", 'blank': 'True'}),
            'training_purpose': ('django.db.models.fields.TextField', [], {'db_column': "'TRAINING_PURPOSE'", 'blank': 'True'}),
            'training_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'TRAINING_START_DATE'"}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"})
        },
        'dashboard.traininganimatorstrained': {
            'Meta': {'object_name': 'TrainingAnimatorsTrained', 'db_table': "u'TRAINING_animators_trained'"},
            'animator': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Animator']", 'db_column': "'animator_id'"}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'training': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Training']", 'db_column': "'training_id'"})
        },
        'dashboard.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'district_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.District']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region_operated': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Region']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'dashboard.video': {
            'Meta': {'unique_together': "(('title', 'video_production_start_date', 'video_production_end_date', 'village'),)", 'object_name': 'Video', 'db_table': "u'VIDEO'"},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ACTORS'"}),
            'approval_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'APPROVAL_DATE'", 'blank': 'True'}),
            'audio_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'AUDIO_QUALITY'", 'blank': 'True'}),
            'cameraoperator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'cameraoperator'", 'to': "orm['dashboard.Animator']"}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'db_column': "'DURATION'", 'blank': 'True'}),
            'edit_finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_FINISH_DATE'", 'blank': 'True'}),
            'edit_start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EDIT_START_DATE'", 'blank': 'True'}),
            'editing_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'EDITING_QUALITY'", 'blank': 'True'}),
            'facilitator': ('dashboard.fields.BigForeignKey', [], {'related_name': "'facilitator'", 'to': "orm['dashboard.Animator']"}),
            'farmers_shown': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Person']", 'symmetrical': 'False'}),
            'final_edited_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'FINAL_EDITED_FILENAME'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'language': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Language']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'movie_maker_project_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'MOVIE_MAKER_PROJECT_FILENAME'", 'blank': 'True'}),
            'picture_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'PICTURE_QUALITY'", 'blank': 'True'}),
            'raw_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'RAW_FILENAME'", 'blank': 'True'}),
            'related_agricultural_practices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dashboard.Practices']", 'symmetrical': 'False'}),
            'remarks': ('django.db.models.fields.TextField', [], {'db_column': "'REMARKS'", 'blank': 'True'}),
            'reviewer': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Reviewer']", 'null': 'True', 'blank': 'True'}),
            'storybase': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'STORYBASE'"}),
            'storyboard_filename': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'db_column': "'STORYBOARD_FILENAME'", 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'db_column': "'SUMMARY'", 'blank': 'True'}),
            'supplementary_video_produced': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'null': 'True', 'blank': 'True'}),
            'thematic_quality': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'THEMATIC_QUALITY'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'TITLE'"}),
            'video_production_end_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_END_DATE'"}),
            'video_production_start_date': ('django.db.models.fields.DateField', [], {'db_column': "'VIDEO_PRODUCTION_START_DATE'"}),
            'video_suitable_for': ('django.db.models.fields.IntegerField', [], {'db_column': "'VIDEO_SUITABLE_FOR'"}),
            'video_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'db_column': "'VIDEO_TYPE'"}),
            'viewers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Village']"}),
            'youtubeid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'YOUTUBEID'", 'blank': 'True'})
        },
        'dashboard.videoagriculturalpractices': {
            'Meta': {'object_name': 'VideoAgriculturalPractices', 'db_table': "u'VIDEO_related_agricultural_practices'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'practice': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Practices']", 'db_column': "'practices_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.videosscreenedinscreening': {
            'Meta': {'object_name': 'VideosScreenedInScreening', 'db_table': "u'SCREENING_videoes_screened'"},
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'screening': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Screening']", 'db_column': "'screening_id'"}),
            'video': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Video']", 'db_column': "'video_id'"})
        },
        'dashboard.village': {
            'Meta': {'unique_together': "(('village_name', 'block'),)", 'object_name': 'Village', 'db_table': "u'VILLAGE'"},
            'block': ('dashboard.fields.BigForeignKey', [], {'to': "orm['dashboard.Block']"}),
            'control': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'CONTROL'", 'blank': 'True'}),
            'id': ('dashboard.fields.BigAutoField', [], {'primary_key': 'True'}),
            'no_of_households': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'NO_OF_HOUSEHOLDS'", 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'POPULATION'", 'blank': 'True'}),
            'road_connectivity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'ROAD_CONNECTIVITY'", 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'START_DATE'", 'blank': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'VILLAGE_NAME'"})
        }
    }

    complete_apps = ['dashboard']
