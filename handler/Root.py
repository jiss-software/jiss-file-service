import logging
import tornado
import time
from bson.json_util import dumps
from tornado.options import options


class RootHandler(tornado.web.RequestHandler):
    logger = logging.getLogger('/')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        self.logger.info('Request to file upload')

        collection = self.settings['db']['Files']

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

                yield collection.save(data)
                result.append(data)

        self.write(dumps(result))

