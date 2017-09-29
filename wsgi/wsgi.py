from wsgiref.simple_server import make_server

def web_application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return 'Hello, world!'

httpd = make_server('', 5000, web_application)

print 'Serving http on port 5000'
httpd.serve_forever()

