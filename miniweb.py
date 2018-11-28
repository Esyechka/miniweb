# general imports
import json
import os
from urllib.parse import urlparse

# constants
TEMPLATE_PATH = 'templates' #todo move to settings

def HttpResponse(request, response_str):
    """encode response_str with ascii encoding for HTTP return value"""
    request.setHeader(b"content", b"text/plain")
    return(response_str.encode("ascii"))

def JsonResponse(request, obj):
    """dump response_obj to json and encode with ascii encoding for API return value"""
    response_json = json.dumps(obj)
    request.setHeader(b"content", b"application/json")
    return(response_json.encode("ascii"))

def template_loader(template_name):
    """Load and return template content as string

    Look for file matching template_name in templates folder.
    Return content of file as template
    Display template not found msg on error
    """
    try:
        fn = os.path.join(TEMPLATE_PATH, template_name)
        with open(fn, 'r') as f:
            template = f.read()
            return template
    except Exception:
        print ("template not found:", template_name)
        raise
    # else:
    #     return template


#todo change to render(template, context)
def render(request, template_name, context):
    """Render template with context and return result string as HttpResponse
    
    template_name: template file under template_path
    context: dict of context key/value pairs for template variables
    """
    template = template_loader(template_name)
    filled_template = template.format(**context)
    return HttpResponse(request, filled_template)


