
class Request_Middleware_Manager():
    """Manage middleware request processing interactions 

    each middleware in Request_Middleware_Manager process request in turn
    and return a request object for subsequent middleware or view
    """

    def __init__(self):
        """Initialize middleware pipeline list"""
        self.middlewares = []

    def add_middleware(self, middleware):
        """Append middleware to processing pipeline"""
        self.middlewares.append(middleware)

    def process(self, request):
        """Process request through all middleware
        
        each middleware is called in turn to process request object
        middleware return a request object for subsequent middleware or view
        """
        for middleware in self.middlewares:
            request = middleware(request)
        return request


class Response_Middleware_Manager():
    """Manage middleware response processing interactions 

    each middleware in Response_Middleware_Manager process response in turn
    and return a response object for subsequent middleware
    """

    def __init__(self):
        """Initialize middleware pipeline list"""
        self.middlewares = []

    def add_middleware(self, middleware):
        """Append middleware to processing pipeline"""
        self.middlewares.append(middleware)

    def process(self, response):
        """Process request through all middleware
        
        each middleware is called in turn to process response object 
        middleware return a response object for subsequent middleware 
        """
        for middleware in self.middlewares:
            response = middleware(response)
        return response
