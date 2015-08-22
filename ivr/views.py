from django.http import HttpResponse
from django.views.generic import View



def thanks_view(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Call finished : Call id : %s , videoId : %s",callSid,videoId)
    response = HttpResponse(videoDetails[int(videoId)][4],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response
