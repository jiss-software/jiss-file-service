import tornado.ioloop
import tornado.web
import logging
from handler import HealthCheckHandler, RootHandler, NameHandler
import motor
from tornado.options import define, options
import os

define("port", default=33003, help="Application port")
define("db_address", default="mongodb://localhost:27017", help="Database address")
define("db_name", default="Files", help="Database name")
define("max_buffer_size", default=50 * 1024**2, help="")
define("log_dir", default="log", help="Logger directory")
define("files_dir", default="files", help="Files directory")

if not os.path.exists(options.log_dir):
    os.makedirs(options.log_dir)

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='log/server.log',
    level=logging.DEBUG
)

ioLoop = tornado.ioloop.IOLoop.current()
mongodb = ioLoop.run_sync(motor.MotorClient(options.db_address).open)

context = dict(
    logger=logging.getLogger('HealthCheck'),
    mongodb=mongodb
)

app = tornado.web.Application([
    (r"/", HealthCheckHandler, context),
    (r"/files", RootHandler, context),
    (r"/files/([^/]*)", NameHandler, context),
], autoreload=True)

app.listen(options.port)

if __name__ == "__main__":
    try:
        logging.info("Starting HTTP proxy on port %d" % options.port)
        ioLoop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server HTTP proxy on port %d" % options.port)
        ioLoop.stop()
