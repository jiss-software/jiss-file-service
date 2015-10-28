import tornado
import time
from bson.json_util import dumps
from tornado.options import options


class RootHandler(tornado.web.RequestHandler):
    def initialize(self, logger, mongodb):
        self.logger = logger
        self.mongodb = mongodb[options.db_name]['Files']

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.logger.info('Request to file upload')

        result = []

        for item in self.request.files.values():
            for file_info in item:
                timestamp = time.time()

                data = {
                    'name': '%s-%s' % (timestamp, file_info['filename']),
                    'location': 'TBD',
                    'context': 'context',
                    'realName': file_info['filename'],
                    'mimeType': file_info['content_type'],
                    'deleted': False,
                    'timestamp': timestamp,
                    'restrictions': {
                        'quota': False,
                        'session': False
                    }
                }

                self.logger.info('File uploaded: %s with mime type %s' % (data['realName'], data['mimeType']))

                with open('%s/%s' % (options.files_dir, data['name']), 'w') as f:
                    f.write(file_info['body'])

                self.logger.info('File saved at %s' % data['name'])

                yield self.mongodb.save(data)
                result.append(data)

        self.write(dumps(result))

