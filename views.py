# general imports
import json
from urllib.parse import urlparse

# miniweb imports
import miniweb

class API_View():
    """Class for serving JSON data to API requests

    Registered objects are made available via URI path objname/
    Return JSON response of requested data
    """
    def __init__(self):
        """Initialize data store in self.data"""
        self.data = {}
        
    def parse_uri(self, request):
        """Decode and parse URI for path segments
        
        URI /api/books becomes ['api', 'books']
        return list of path segments
        """
        # decode ascii
        uri = request.uri.decode(encoding='ascii')
        # get path
        path = urlparse(uri).path
        # split into / delimited segments
        path_segments = str(path)[1:].split('/')
        return path_segments
        
    def view(self, request):
        """Decode request URI for object and return JSON
        
        Object name is 2nd element in path segments
        return JsonResponse of requested object data
        """
        # get path_segments
        path_segments = self.parse_uri(request)
        # check for path segment length. It should be >= 2
        # less than 2 means it is missing required object name
        if len(path_segments) < 2:
            err = {'error': 'no object name specified in url'}
            return miniweb.JsonResponse(request, err)

        # verify object name exists. return error if not
        name = path_segments[1]
        if name not in self.data:
            err = {'error': 'no object name specified in url'}
            return miniweb.JsonResponse(request, err)

        # retrieve data object by name
        obj = self.data[name]            
        return miniweb.JsonResponse(request, obj)

    def register_data(self, name, obj):
        """Register data obj for serving as JSON

        object is made available at name/ URI
        """ 
        self.data[name] = obj

def book_data_sample():
    """Load and return sample data (list of books)"""
    books = []
    with open('books.ndjson', 'r') as f:
        # decode line delimited JSON
        books = [json.loads(line) for line in f]
    return books

def make_api_view():
    """Factory for creating example API_View 
    
    Create new API_View object. Load sample books data
    Return API_View.view to use as view in urls.py
    """
    # get  sample books data
    books = book_data_sample()
    api_view = API_View()
    # register sample data
    api_view.register_data('books', books)
    # return view method of API_View
    return api_view.view

def birds(request):
    """Example view for JSON"""
    flightless_birds = {'penguins': ['African penguin', 'King penguin', 'Adélie penguin'],
                        'kiwis': ['great spotted kiwi', 'little spotted kiwi', 'Okarito kiwi', 'southern brown kiwi', 'North Island brown kiwi'],
                        'cassowary': [' southern cassowary', 'Dwarf cassowary', 'Northern cassowary'],
                        }
    context = {'kiwis': ['great spotted kiwi', 'little spotted kiwi', 'Okarito kiwi', 'southern brown kiwi', 'North Island brown kiwi']}
    return miniweb.JsonResponse(request, context)

def view_exception(request):
    """Example view for template"""
    # this view is used to demonstrate 500 server error with traceback on a broken view
    context = {'first_paramete':'name', 'second_parameter':'grand penguin'}
    return miniweb.render (request, 'secondary.html', context)

# View functions: take request
def viewa(request):
    """Example view for template"""
    context = {'view_name':'landing', 'penguin_type':'grand penguin'}
    return miniweb.render (request, 'landing.html', context)

def viewb(request):
    """Example view for template"""
    context = {'first_parameter':'name', 'second_parameter':'grand penguin'}
    return miniweb.render (request, 'secondary.html', context)

def viewc(request):
    """Example view for template"""
    context = {'first_parameter':'name', 'second_parameter':'grand penguin'}
    return miniweb.render (request, 'secondary.html', context)

