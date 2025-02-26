import time

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.time()

        # Process the request and get the response
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time
        print(f"Request {request.path} took {duration:.4f} seconds")

        return response