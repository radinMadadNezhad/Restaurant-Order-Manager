import logging
import traceback
from django.conf import settings

logger = logging.getLogger('django.request')

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Log the error
        logger.error(
            f"Exception during request: {request.path}\n"
            f"{traceback.format_exc()}"
        )
        
        # In debug mode, we let Django's built-in error handling take over
        # In production, we could return a custom error page
        return None 