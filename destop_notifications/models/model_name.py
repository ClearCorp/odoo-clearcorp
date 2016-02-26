# -*- coding: utf-8 -*-
# © <2016> ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


def websocket_app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
        message = ws.receive()
        ws.send(message)

server = pywsgi.WSGIServer(("", 8000), websocket_app,
                            handler_class=WebSocketHandler)
server.serve_forever()
