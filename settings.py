from tornado.options import define, options
from handler import HealthCheckHandler, RootHandler, NameHandler
import os

define("port", default=33003, help="Application port")
define("db_address", default="mongodb://localhost:27017/?serverSelectionTimeoutMS=2000&socketTimeoutMS=2000&connectTimeoutMS=2000", help="Database address")
define("db_name", default="Files", help="Database name")
define("max_buffer_size", default=50 * 1024**2, help="")
define("autoreload", default=False, help="Autoreload server on change")

define("log_dir", default="log", help="Logger directory")
define("log_file", default="jiss-file-service.log", help="Logger file name")
define("files_dir", default="files", help="Files directory")

if not os.path.exists(options.files_dir):
    os.makedirs(options.files_dir)

routing = [
    (r"/", HealthCheckHandler),
    (r"/files", RootHandler),
    (r"/files/([^/]*)", NameHandler),
]
