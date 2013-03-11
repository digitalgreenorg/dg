import json, urllib2
from django.http import HttpResponse

def get_search_completion(request):
    query_string = request.GET['query']
    url = ' http://localhost:9200/website/searchcompletion/_search'
    filter_dict = {}
    data =  json.dumps({
                        "query" : {"term" : { "text" : query_string}},
                        "fields" : ["type","text","url"],
                        "highlight" : {"fields" : {"text" : {}}}
                        })
    request = urllib2.Request(url)
    request.get_method = lambda: 'GET'
    try:
        result = urllib2.urlopen(request, data)
    except Exception,ex:
        pass
    data = json.loads(result.read())
    if data['hits']['hits']:
        return HttpResponse(data['hits']['hits'], mimetype="application/json")
    else:
        return HttpResponse("0")
        
def get_search_collection(request):
    filter_dict = {}
    if request.POST:
        print request.POST
        query_string = request.POST.get('searchString')
        selections = {}
        if query_string:
            selections["title"] = query_string
        sort = request.POST.get('orderBy')
        if sort:
            filter_dict["sort"] = [{sort : {"order" : "desc"} }]
        filters = request.POST.get('filters')
        print filters
        facets = ["country", "state", "language", "partner", "category", "subcategory", "topic", "subject"]
        if filters:
            for facet in facets:
                if facet in filters:
                    print filters
                    # basically put a filter
                    selections[facet] = filters[facet]
                else:
                    pass
                    # put a facet
        filter_dict["query"] = {"term" : selections}
    url = ' http://localhost:9200/website/searchcollection/_search'
    data =  json.dumps(filter_dict)
    print filter_dict
    request = urllib2.Request(url)
    request.get_method = lambda: 'GET'
    try:
        result = urllib2.urlopen(request, data)
    except Exception,ex:
        pass
    data = json.loads(result.read())
    print data
    hits = data['hits']['hits']
    collections = [a["_source"] for a in hits]
    if collections:
        return HttpResponse(json.dumps({"collections": collections, "totalCount": data['hits']['total']}), mimetype="application/json")
    else:
        return HttpResponse("0")

