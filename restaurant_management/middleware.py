import logging
import traceback
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Log the error
            logger.error(f"Error processing request: {e}")
            logger.error(traceback.format_exc())
            
            # Only in debug mode, provide detailed error
            from django.conf import settings
            if settings.DEBUG:
                return HttpResponse(
                    f"<h1>Error</h1><p>{str(e)}</p><pre>{traceback.format_exc()}</pre>",
                    content_type="text/html",
                    status=500
                )
            # In production, let the standard error handlers take over
            raise 