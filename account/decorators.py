from django.shortcuts import redirect

def user_not_authenticated(function=None, redirect_url='/'):
    """
    Checks if user is authenticated otherwise redirects to homepage
    """
    def decorator(f):
        def _wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            
            return f(request, *args, **kwargs)
        
        return _wrapper

    if function:
        return decorator(function)

    return decorator