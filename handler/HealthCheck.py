import tornado.web
import tornado.gen
import json
import logging


class HealthCheckHandler(tornado.web.RequestHandler):
    logger = logging.getLogger('HealthCheck')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.logger.info('Request to health check')

        components = {
            'mongodb': None
        }

        components['mongodb'] = yield self.settings['db'].alive()

        for key in components:
            if components[key] is None:
                components[key] = False

        result = json.dumps({
            'status': False not in components.values(),
            'components': components
        })

        self.logger.info('Response for health check: %s' % result)
        self.write(result)
