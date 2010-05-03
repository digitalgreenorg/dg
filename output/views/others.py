#Mindless views for plain HTML pages on the main website

def base_career(request):   
    return render_to_response('base_career.html')


def base_contact(request):   
    return render_to_response('base_contact.html')


def base_career_immediate(request):   
    return render_to_response('base_career_immediate.html')