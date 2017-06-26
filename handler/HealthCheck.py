import core
import tornado


class HealthCheckHandler(core.BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.logger.info('Request to health check')

        components = {
            'mongodb': None
        }

        try:
            components['mongodb'] = yield self.settings['db'].is_mongos
        except:
            pass

        for key in components:
            if components[key] is None:
                components[key] = False

        self.response_json({
            'status': False not in components.values(),
            'components': components,
            'version': self.settings['version'],
            'started': self.settings['started']
        })
