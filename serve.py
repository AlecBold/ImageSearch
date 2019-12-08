#! /usr/bin/python3

import re
import os
import io
import cgi
import mimetypes

from model import PredictModel, get_names_of_images
from http.server import HTTPServer, BaseHTTPRequestHandler

IP = 'localhost'
PORT_NUMBER = 3000
SERVER_ADDRESS = (IP, PORT_NUMBER)

class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.predict_model = PredictModel()
        self.search_entities = get_names_of_images()
        super().__init__(*args, **kwargs)

    CLIENT_FILES = {
        '/': 'client/index.html',
        '/index.html': 'client/index.html',
        '/style.css': 'client/style.css',
    }

    MEDIA_PATH = r'\/media\/images\/(\w|\d)+\.(png|jpg|jpeg)$'

    SIMILAR_IMAGES_TEMPLATE = '''\
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <link href="https://fonts.googleapis.com/css?family=Oswald:300,400,500&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="./style.css">
            <title>HotDog</title>
        </head>
        <body>
            <h1>Similar Images</h1>
            <ul>
                %(images)s
            </ul>
        </body>
        </html>
    '''

    def __set_headers(self, content_type, content_length):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Content-Length', content_length)
        self.end_headers()

    def __resolve_get_path(self):
        file_path = os.curdir + os.sep

        if self.path in self.CLIENT_FILES:
            return file_path + self.CLIENT_FILES[self.path]

        if re.match(self.MEDIA_PATH, self.path):
            return file_path + self.path

        return None 

    def do_GET(self):
        file_path = self.__resolve_get_path()

        if not(file_path):
            self.send_error(404, f'File Not Found: {self.path}')
            return

        try: 
            content_type, _ = mimetypes.guess_type(file_path)

            with open(file_path, 'rb') as file_binary:
                file = file_binary.read() 
                self.__set_headers(content_type, int(len(file)))
                self.wfile.write(file)

        except IOError:
            self.send_error(404, f'File Not Found: {self.path}')

            
    def do_POST(self):
        if self.path == '/similar':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )

            image = form['image']
            image_data = image.file.read()

            # function to find similar will be there
            sim_images, distances = self.predict_model.search_nearest(self.search_entities, image_data)
            similar_images = '\n'.join(map(
                lambda img, dist: f'<li><img src="/media/images/{img}"/><div>distance:{dist}</div></li>',
                sim_images, distances
            ))

            content = ( self.SIMILAR_IMAGES_TEMPLATE %  
                        {'images': similar_images})

            body = content.encode('UTF-8', 'replace')
            self.__set_headers('text/html;charset=utf-8', int(len(body)))

            self.wfile.write(body)

try:
    server = HTTPServer(SERVER_ADDRESS, Handler)
    print('Started httpserver on port ', PORT_NUMBER)

    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
