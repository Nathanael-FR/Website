# decorators.py
from django.shortcuts import redirect

def admin_forbiden(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
