from static_site_views import *
import re


#Dictionary for aliasing, all entries have to string-string pair.
global_dict = dict(
getScreening = 'get_screening',
)

#Special route for /analytics/..., all analytics views are imported here.
def analytics_route(request, func_name):
    from output.views.overview_analytics import *
    from output.views.screening_analytics import *
    from output.views.video_analytics import *
    from output.views.adoption_analytics import *
    from output.views.targets import *
    from output.views.common import drop_down_val, overview_line_graph    
    return locals()[func_name](request)

#MAIN Route, urls.py routes everything except admin to this function.
#It firt checks for alias in global_dict.
#Then it checks for patterns 'analytics/..'
#else it calls the view with the recieved 'func_name'
def route(request, func_name):
    if(func_name == ''):
        return home(request)
    if(func_name in global_dict):
        func_name = glocal_dict['func_name']
    else:
        x = re.match('analytics/(.+)',func_name, re.I)
        if(x):
            return analytics_route(request, x.group(1))
        
    return globals()[func_name](request)

