# miniweb imports
from views import *

"""
Declare URI path and corresponding views for handling them
"""

routes = {
    'a': viewa, 
    'b': viewb, 
    'c': viewc,
    'exception': view_exception,
    'api': make_api_view(),
    'birds': birds,
    }
