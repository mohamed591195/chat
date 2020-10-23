from django.http import JsonResponse

def is_ajax_authenticated_post(f):
    
    def wrapper(request, *args, **kwargs):

        if all([request.is_ajax(), request.method == 'POST', request.user.is_authenticated]):

            return f(request, *args, **kwargs)

        return JsonResponse(data={}, status=400)
        
    
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    
    return wrapper