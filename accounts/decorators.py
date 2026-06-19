from django.core.exceptions import PermissionDenied

# Custom decorator to check if user has required roles
def role_required(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                allowed_roles = list(roles)
                # Map 'admin' permission to also include 'service_advisor'
                if 'admin' in allowed_roles and 'service_advisor' not in allowed_roles:
                    allowed_roles.append('service_advisor')
                if request.user.role in allowed_roles or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
