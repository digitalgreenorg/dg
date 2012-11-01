import urllib2

print "Fetching ..."
opener = urllib2.build_opener(urllib2.HTTPHandler)
opener.addheaders =[('User-agent', 'Mozilla/5.0'),
                     ('user', 'yash@digitalgreen:digitalgreen'),
                     ('Cookie', 'csrftoken=2b49a2f48be1fe70eb7f265f3fbc340a; sessionid=f0890bb4bb246575bdb9c51803c25853; __utma=166502700.1959187201.1343713513.1351508888.1351574456.43; __utmb=166502700.7.9.1351574482282; __utmc=166502700; __utmz=166502700.1349328641.37.2.utmcsr=nlnet|utmccn=div2r1|utmcmd=email')]
response = opener.open('https://www.commcarehq.org/a/digitalgreencocomobile/fixtures/data-types/')
print "Data Types Retrieved"
string_response = response.read() 

types = string_response.split('fields')
ids_to_delete = []
for i in range(len(types)-1):
    ids_to_delete.append(types[i+1].partition('_id": "')[2].partition('"}')[0])

if len(ids_to_delete) == 0:
    print "Nothing to delete"
else:    
    for id in ids_to_delete:
        try:
            request_string = 'https://www.commcarehq.org/a/digitalgreencocomobile/fixtures/data-types/' + str(id)
            request = urllib2.Request(request_string)
            request.get_method = lambda: 'DELETE'
            url = opener.open(request)
            print "Deleted item : " + str(id)
        except Exception as ex:
            print " Could not delete item : " + str (id)
