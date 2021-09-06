def set_session(request,key_name,key_value):
    request.session[key_name] = key_value
    
def destroy_session(request,key_name):
    del request.session[key_name]
    request.session.modified = True