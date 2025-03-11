from django.shortcuts import redirect
from django.http import Http404
import logging

logger = logging.getLogger("checker")
debug_logger = logging.getLogger("debug")
info_logger = logging.getLogger("info")
warning_logger = logging.getLogger("warning")
error_logger = logging.getLogger("error")
critical_logger = logging.getLogger("critical")


class ErrorHandlingMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in (400, 401, 403, 404, 500):
            print("an error occured")
            logger.warning(f"error page is called: status code {response.status_code}, user {request.user}")
            return redirect("error_page")
        return response


class DebugLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        info_logger.debug("Request: %s" % request)
        return self.get_response(request)


class InfoLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        info_logger.info("Request: %s" % request)
        return self.get_response(request)


class WarningLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        warning_logger.warning("Request: %s" % request)
        return self.get_response(request)


class CriticalLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        critical_logger.critical("Request: %s" % request)
        return self.get_response(request)
