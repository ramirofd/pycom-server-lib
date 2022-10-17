class Response:
    def __init__(self, code, content_type, body):
        self.code = code
        self.content_type = content_type
        self.body = body

    def __str__(self):
        return "HTTP/1.1 {code}\r\nContent-Type: {content_type}\r\nConnection:close \r\n\r\n{body}"\
            .format(code=self.code, content_type=self.content_type, body=self.body)


class Response200(Response):
    def __init__(self, content_type='text/plain', body=''):
        super(Response200, self).__init__('200 OK', content_type, body)


class Response404(Response):
    def __init__(self, content_type='text/plain', body=''):
        super(Response404, self).__init__('404 Not Found', content_type, body)


class Response400(Response):
    def __init__(self, content_type='text/plain', body=''):
        super(Response400, self).__init__('400 Bad Request', content_type, body)


class Response500(Response):
    def __init__(self, content_type='text/plain', body=''):
        super(Response500, self).__init__('500 Internal Server Error', content_type, body)


class JsonResponse200(Response200):
    def __init__(self, body):
        super(JsonResponse200, self).__init__('application/json', body)


class JsonResponse400(Response400):
    def __init__(self, body):
        super(JsonResponse400, self).__init__('application/json', body)


class JsonResponse404(Response404):
    def __init__(self, body):
        super(JsonResponse404, self).__init__('application/json', body)


class JsonResponse500(Response500):
    def __init__(self, body):
        super(JsonResponse500, self).__init__('application/json', body)