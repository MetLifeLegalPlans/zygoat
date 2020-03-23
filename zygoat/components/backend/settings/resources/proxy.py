class ReverseProxyHandlingMiddleware(object):
    """
    Normalize all incoming IP addresses from the load balancer
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META:
            ip = request.META["HTTP_X_FORWARDED_FOR"]
        else:
            ip = request.META["REMOTE_ADDR"]

        request.META["REMOTE_ADDR"] = ip.split(",")[0]

        return self.get_response(request)
