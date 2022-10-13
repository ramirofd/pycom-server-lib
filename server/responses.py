class Response:
    def __init__(self, code, content_type, body):
        self.code = code
        self.content_type = content_type
        self.body = body


class Response200(Response):
    def __init__(self, content_type, body):
        super(Response200, self).__init__('200 OK', content_type, body)


class Response404(Response):
    def __init__(self, content_type, body):
        super(Response404, self).__init__('404 Not Found', content_type, body)


class JsonResponse200(Response200):
    def __init__(self, body):
        super(JsonResponse200, self).__init__('application/json', body)


class JsonResponse404(Response):
    def __init__(self, body):
        super(JsonResponse404, self).__init__('application/json', body)
