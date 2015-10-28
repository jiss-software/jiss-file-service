import os
import tornado
from tornado.options import options


class NameHandler(tornado.web.RequestHandler):
    def initialize(self, logger, mongodb):
        self.logger = logger
        self.mongodb = mongodb[options.db_name]['Files']

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, name):
        self.logger.info('Request to file download')

        locator = '%s/%s' % (options.files_dir, name)
        if not os.path.isfile(locator):
            self.set_status(404)
            return

        file_info = yield self.mongodb.find_one({'name': name})
        if not file_info or 'deleted' in file_info and file_info['deleted']:
            self.set_status(404)
            return

        self.set_header('Content-Type', file_info['mimeType'])

        # TODO: Check here restrictions of access
        with open(locator, 'rb') as f:
            data = f.read()
            self.write(data)

        self.finish()
