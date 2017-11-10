import uuid

from tornado import web
import sprockets.http

from tornado_tutorial.app import (
    ThresholdCollectionHandler,
    ThresholdResourceHandler,
)

re_uuid = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def make_app(**settings):
    return web.Application([
        (r"/threshold/(?P<threshold_id>{u}?)/".format(u=re_uuid),
            ThresholdResourceHandler),
        (r"/threshold/", ThresholdCollectionHandler),
    ], **settings)

if __name__ == '__main__':
    sprockets.http.run(make_app)
