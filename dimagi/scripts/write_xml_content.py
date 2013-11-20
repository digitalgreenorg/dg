def write_opening_meta(file, num_people):
    file.write('<?xml version="1.0" ?>\n')
    file.write('<data uiVersion="1" version="8" name="New Form" xmlns:jrm="http://dev.commcarehq.org/jr/xforms" xmlns="http://openrosa.org/formdesigner/DB63E17D-B572-4F5B-926E-061583DAE9DA">\n')
    file.write('<num_people> %s </num_people>\n' % (unicode(num_people)))
    
def write_person_content(file, i, case_id, owner_id, person, videos_seen, videos_adopted):
    file.write('<people>\n')
    file.write('<n'+unicode(i)+':case case_id="' + unicode(case_id)+ '" date_modified="'+ unicode(datetime.datetime.now().date()) + '" user_id="' + owner_id + '" xmlns:n'+unicode(i)+'="http://commcarehq.org/case/transaction/v2">\n')
    file.write('<n'+unicode(i)+':create>\n')
    file.write('<n'+unicode(i)+':case_type>person</n'+unicode(i)+':case_type>\n')
    file.write('<n'+unicode(i)+':owner_id>'  + owner_id + '</n'+unicode(i)+':owner_id>\n')
    file.write('<n'+unicode(i)+':case_name>' + unicode(person.person_name) + '</n'+unicode(i)+':case_name>\n')
    file.write('</n'+unicode(i)+':create>\n')
    file.write('<n'+unicode(i)+':update>\n')
    file.write('<n'+unicode(i)+':id>' + unicode(person.id) + '</n'+unicode(i)+':id>\n')
    file.write('<n'+unicode(i)+':group_id>' + unicode(person.group.id)+ '</n'+unicode(i)+':group_id>\n')
    file.write('<n'+unicode(i)+':videos_seen>' + videos_seen + '</n'+unicode(i)+':videos_seen>\n')
    file.write('<n'+unicode(i)+':videos_adopted>' + videos_adopted + '</n'+unicode(i)+':videos_adopted>\n')
    file.write('</n'+unicode(i)+':update>\n')
    file.write('</n'+unicode(i)+':case>\n')
    file.write('</people>\n')
    
def write_closing_meta(file, owner_id, i):
    file.write('<n'+unicode(i) + ':meta xmlns:n' + unicode(i) + '="http://openrosa.org/jr/xforms">\n')
    file.write('<n'+unicode(i) + ':userID>'+unicode(owner_id) + '</n' + unicode(i) + ':userID>\n')
    file.write('<n'+unicode(i) + ':instanceID>' + unicode(uuid.uuid4()) + '</n' + unicode(i) + ':instanceID>\n')
    file.write('</n' + unicode(i) + ':meta>\n')
    file.write('</data>')
    