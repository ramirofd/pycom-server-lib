import socket
# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Server:
    base_url = '192.169.0.105'
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

server = Server()

@server.post('/info')
def print_rama(json: str):
    return f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection:close \r\n\r\n {json}'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 8000

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        # request = client_connection.recv(1024).decode()
        # print(request.split(' ')[0], request.split(' ')[1],request[request.find('\r\n\r\n')+4:])
        server.get_client_thread()(client_connection, client_address)
        # Send HTTP response
        # response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n'
        # client_connection.sendall(response.encode())
        # client_connection.close()

    # Close socket
    server_socket.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
