from django.http import HttpResponseForbidden

def admin_v8_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        # Check if user is logged in and has the required email address
        if request.user.is_authenticated and request.user.email == 'adminv8redroy@gmail.com':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You don't have permission to access this page.")
    return wrapped_view
