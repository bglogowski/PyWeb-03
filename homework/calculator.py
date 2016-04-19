#!/usr/bin/env python3

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""



def help():

    help_html = """
    calculator.py supports the following operations:
    <ul>
    <li>Addition</li>
    <li>Subtraction</li>
    <li>Multiplication</li>
    <li>Division</li>
    </ul><br>
    Examples:<br>
    http://localhost:8080/multiply/3/5   => 15<br>
    http://localhost:8080/add/23/42      => 65<br>
    http://localhost:8080/subtract/23/42 => -19<br>
    http://localhost:8080/divide/22/11   => 2<br>
    http://localhost:8080/divide/6/0     => HTTP '400 Bad Request'<br>"""

    return help_html.encode('utf8')


def html_format(text):
    """
    Formats answers to return to the HTTP client
    """
    return str(text).encode('utf8')

def add(x, y):
    return(html_format(x + y))

def subtract(x, y):
    return(html_format(x - y))

def multiply(x, y):
    return(html_format(x * y))

def divide(x, y):
    """
    Should return the integer result of dividing two numbers
    """
    try:
        answer = x / y
    except:
        raise ValueError
    return(html_format(int(answer)))


# Map the command strings to functions
func_map = { 'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide
           }


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    p = path.strip('/').split('/')

    if len(p) < 3:
        return help()

    elif len(p) == 3:
        f = func_map[str(p[0])]
        x = int(p[1])
        y = int(p[2])
        return f(x, y)

    else:
        raise NameError



def application(environ, start_response):

    headers = [('Content-type', 'text/html; charset=utf-8')]

    try:
        path = environ.get('PATH_INFO', None)
        body = resolve_path(path)
        status = '200 OK'

    except ValueError:
        status = '400 Bad Request'
        body = '<b>400</b> Bad Request<p><i>The server will not process the request due to an apparent client error.</i></p>'.encode('utf8')
        body += help()

    except NameError:
        status = '404 Not Found'
        body = '<b>404</b> Not Found<p><i>The requested resource could not be found.</i></p>'.encode('utf8')
        body += help()

    except Exception:
        status = '500 Internal Server Error'
        body = '<b>500</b> Internal Server Error<p><i>An unexpected condition was encountered.</i></p>'.encode('utf8')
        body += help()

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)

        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

