from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
import json
from datetime import datetime

# MongoDB Atlas connection details
MONGO_CONNECTION_STRING = 'mongodb+srv://amirhoseinfj:sa9avcsHWeT61u7M@amoolinux.mimk6ci.mongodb.net/?retryWrites=true&w=majority'
DATABASE_NAME = 'reservation_db'
COLLECTION_NAME = 'reservations'

client = MongoClient(MONGO_CONNECTION_STRING)
db = client[DATABASE_NAME]
reservations_collection = db[COLLECTION_NAME]

class JSONEncoder(json.JSONEncoder):
    """Extend json.JSONEncoder to serialize datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format datetime objects as strings
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class ReservationServer(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/reservations':
            reservations = list(reservations_collection.find({}, {'_id': False}))
            # Use the custom JSONEncoder to serialize the data
            response = json.dumps({'reservations': reservations}, cls=JSONEncoder).encode('utf-8')
            self._set_headers()
            self.wfile.write(response)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/reservations':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            reservations_collection.insert_one(post_data)
            self._set_headers(201)
            self.wfile.write(json.dumps({'message': 'Reservation created successfully'}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/reservations/'):
            reservation_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            put_data = json.loads(self.rfile.read(content_length))
            reservations_collection.update_one({'reservation_id': reservation_id}, {'$set': put_data})
            self._set_headers(200)
            self.wfile.write(json.dumps({'message': 'Reservation modified successfully'}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/reservations/'):
            reservation_id = self.path.split('/')[-1]
            result = reservations_collection.delete_one({'reservation_id': reservation_id})
            if result.deleted_count > 0:
                self._set_headers(204)
            else:
                self._set_headers(404, 'application/text')
                self.wfile.write('Reservation not found'.encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_OPTIONS(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=ReservationServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
