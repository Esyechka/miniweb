# general imports
import traceback
from urllib.parse import urlparse

# miniweb imports
from miniweb import render

class Router():
    """URI Router. routes URI to view registered to handle it 

    Router parses URI from requests, and finds the view registered to URI.
    If no view is registered, return 404 Response
    """
    def __init__(self, routes=None):
        """Create Router with initial URI/view routes

        routes is a dict with URI strings as keys, views as values
        Views are functions that accepts a Request and returns HttpResponse
        """
        # store self.paths URL/view mapping
        self.paths = {}
        if routes is not None:
            self.set_routes(routes)

    def set_routes(self, new_routes):
        """Register views to handle URIs

        routes is a dict with URI path strings as keys, views as values
        Views are functions that accept Request and return HttpResponse
        new path/view are permitted to override old views
        """

        # merge new_routes into self.path.
        # {**..} is equivalent to loop commented out below
        self.paths = {**self.paths, **new_routes} 

        # for k, v in new_routes.items():
        #     self.paths[k] = v
        
    def uri_parser(self, uri):
        """Parse and return URI components from request
        
        Return tuple of URI path, url params, and query 
        """
        parsed_uri = urlparse(uri)
        return parsed_uri.path[1:], parsed_uri.params, parsed_uri.query

    def route(self, request):
        """Route request to view registered to handle it
        
        each registered view is linked to a unique URI. 
        Route uses URI to dispatch request to view, and accept returned HttpResponse
        Provide stack trace on view errors to assist debugging
        """
        # decode ascii encoded data
        uri = request.uri.decode(encoding='ascii')  
        path, *_ = self.uri_parser(uri)
        path = path.split('/')[0]

        # get registered view for path. If none, use path_not_found
        view = self.paths.get(path, self.path_not_found)

        #handle view errors
        try:
            return view(request)
        except:
            # provide stack trace as HTTP response for debugging
            tb = traceback.format_exc()
            # view error is server 500 error
            return self.server_error(request, tb)

    def path_not_found(self, request):
        """Provide 404 message and registered routes for debugging
        
        display collection of valid paths that have registered views
        return response code 404        
        """
        request.setResponseCode(404)
        # context is collection of valid paths
        context = {'paths': self.paths}
        return render(request, '404.html', context)

    def server_error(self, request, error):
        """Provide stack trace as HttpResponse for debugging
        
        error is stack trace and exception message string
        return response code 500
        """
        request.setResponseCode(500)
        # context is error string
        context = {'error': error}
        return render(request, '500.html', context)



