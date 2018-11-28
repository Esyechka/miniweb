# twisted imports
from twisted.web import server, resource
from twisted.internet import reactor, endpoints

# miniweb imports
import urls
import router
import middleware

PORT = "tcp:8080" 
class Site(resource.Resource):
    """Main object for handing HTTP requests 

    Site is the object twisted will serve with. 
    Each http request will be sent to render_GET() 
    render_GET return HttpResponse for each HTTP request
    """
    # isLeaf flag for twisted. this is the only twisted resource we use
    isLeaf = True  

    def __init__(self):
        """Initialize Router and Middleware Managers
        
        Router routes requests based on URI
        Middleware Managers process request/response
        """
        self.router = router.Router(urls.routes)
        #Request middleware manager
        self.request_middleware = middleware.Request_Middleware_Manager()
        #Response middleware manager
        self.response_middleware = middleware.Response_Middleware_Manager()

    def render_GET(self, request):
        """Main entry point for HTTP requests to our mini web framework 

        request is twisted request object containing HTTP headers and body
        Return HttpResponse
        """
        # print(request.getSession().uid)
        # process request via middlewares
        middleware_request = self.request_middleware.process(request)
        # route to user view
        router_response = self.router.route(middleware_request)
        # process response via middlewares
        middleware_response = self.response_middleware.process(router_response)
        return middleware_response


# serve Site web service using twisted framework at PORT
endpoints.serverFromString(reactor, PORT).listen(server.Site(Site()))
reactor.run()
print("Running on ", PORT)  
