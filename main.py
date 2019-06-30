import socket
from views import *

URLS = {
    '/': index,
    '/blog': blog
}

def bind_addr_to_socket(addr, s):
    try:
        s.bind(addr)
    except:
        print("Address can be binded to the socket")

        exit()

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]

    return (method, url)

def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'

    if code == 405:
        return '<h1>404</h1><p>Method not allowed</p>'

    return URLS[url]()

def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # устанавливаем опцию переиспользования сокета
    # socket.SOL_SOCKET - это указание на сокет server_socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = 'localhost'
    port = 5001

    bind_addr_to_socket((host, port), server_socket)
    server_socket.listen()

    print('Server is listening on port ' + str(port))

    while True:
        try:
            client_socket, addr = server_socket.accept()

            request = client_socket.recv(1024)

            response = generate_response(request.decode('utf-8'))

            client_socket.sendall(response)
            # мы в браузере ничего не увидим, по соединение не будет закрыто
            client_socket.close()
        except:
            print('\nServer stopped listening')

            break

if __name__ == '__main__':
    run()
