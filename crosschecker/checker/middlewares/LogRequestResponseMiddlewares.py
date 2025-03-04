from django.shortcuts import redirect
from django.http import Http404
import logging

logger = logging.getLogger("checker")

class ErrorHandlingMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code in (400, 401, 403, 404, 500) and request.path != '/favicon.ico':
            print("an error occured")
            logger.warning(f"error page is called: status code {response.status_code},user {request.user}")
            return redirect("error_page")

        return response