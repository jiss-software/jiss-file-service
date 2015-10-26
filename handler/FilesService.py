import tornado
import time
from bson.json_util import dumps
from tornado.options import options


class FilesServiceHandler(tornado.web.RequestHandler):
    def initialize(self, logger, mongodb):
        self.logger = logger
        self.mongodb = mongodb

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.logger.info('Request to file upload')

        for item in self.request.files.values():
            file_info = item[0]

            self.logger.info('File uploaded: %s with mime type %s' % (file_info['filename'], file_info['content_type']))
            name = '%s-%s' % (time.time(), file_info['filename'])

            with open('%s/%s' % (options.files_dir, name), 'w') as f:
                f.write(file_info['body'])

            self.logger.info('File saved at %s' % name)

        self.write('done')
