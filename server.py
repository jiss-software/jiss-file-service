import tornado.ioloop
import tornado.web
import logging
import motor
from settings import routing
from tornado.options import options
import os

if not os.path.exists(options.log_dir):
    os.makedirs(options.log_dir)

logging.basicConfig(
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='%s/%s' % (options.log_dir, options.log_file),
    level=logging.DEBUG
)

ioLoop = tornado.ioloop.IOLoop.current()
mongodb = ioLoop.run_sync(motor.MotorClient(options.db_address).open)
app = tornado.web.Application(routing, db=mongodb, autoreload=options.autoreload)

app.listen(options.port)

if __name__ == "__main__":
    try:
        logging.info("Starting HTTP proxy on port %d" % options.port)
        ioLoop.start()
    except KeyboardInterrupt:
        logging.info("Shutting down server HTTP proxy on port %d" % options.port)
        ioLoop.stop()
