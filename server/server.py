

class Server:
    urls = {
        'GET': dict(),
        'POST': dict(),
        'PUT': dict(),
        'DELETE': dict(),
        'PATCH': dict()
    }

    def get(self, path: str):
        def decorator_repeat(func):
            self.urls['GET'][path] = func
        return decorator_repeat

    def post(self, path: str):
        def decorator_repeat(func):
            self.urls['POST'][path] = func
        return decorator_repeat

    def put(self, path: str):
        def decorator_repeat(func):
            self.urls['PUT'][path] = func
        return decorator_repeat

    def delete(self, path: str):
        def decorator_repeat(func):
            self.urls['DELETE'][path] = func
        return decorator_repeat

    def patch(self, path: str):
        def decorator_repeat(func):
            self.urls['PATCH'][path] = func
        return decorator_repeat

    def get_client_thread(self):
        def client_thread(socket, n):
            # request = socket.recv(4096)
            request = socket.recv(4096).decode()
            if len(request) == 0:
                socket.close()
                # return BadRequest
                return
            method = request.split(' ')[0]
            path = request.split(' ')[1]
            body_start = request.find('\r\n\r\n')
            body = ''
            if body_start >= 0:
                body = request[body_start+4:]
            print(f'Request: {method} {path} {body}')
            try:
                funct = self.urls.get(method).get(path)
                if funct is not None:
                    # Build response and send to client
                    response = funct(body)
                    socket.send(response.encode())
                    socket.close()

            except Exception as err:
                # return BadRequest
                pass
        return client_thread