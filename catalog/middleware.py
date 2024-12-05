from catalog.models import Genre, Language


# to display select menus on all pages
class SidebarDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add genres and languages to the request
        request.sidebar_data = {
            "genres": Genre.objects.all(),
            "languages": Language.objects.all(),
        }
        return self.get_response(request)
