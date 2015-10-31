import core
import os
import tornado
from tornado.options import options


class NameHandler(core.BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, name):
        self.logger.info('Request to file download')

        locator = '%s/%s' % (options.files_dir, name)
        if not os.path.isfile(locator):
            self.set_status(404)
            return

        file_info = yield self.settings['db'][options.db_name]['Files'].find_one({'name': name})
        if not file_info or 'deleted' in file_info and file_info['deleted']:
            self.set_status(404)
            return

        self.set_header('Content-Type', file_info['mimeType'])

        # TODO: Check here restrictions of access
        with open(locator, 'rb') as f:
            data = f.read()
            self.write(data)

        self.finish()
        self.logger.info('Sending file located at %s' % locator)
