from django.shortcuts import redirect


class AdminLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("login"):
            pass
        elif (not request.user.is_authenticated) or (
                request.path.startswith('/admin') and not request.user.has_perm('admin.access_admin')):
            print("redirection from path ", request.path)
            return redirect("/")

        return self.get_response(request)
