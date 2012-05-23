from django import template

register = template.Library()

@register.simple_tag
def analytics_get_request(geog, id, get_req_url):
    return_str = ""
    if geog != None:
        return_str = "geog=%s&id=%s" % (geog.lower(), str(id))
    if get_req_url:
        if return_str:
            return_str = return_str + "&" + get_req_url
        else:
            return_str = get_req_url
    
    if return_str:
        return_str = "?" + return_str
    
    return return_str