import uuid

from tornado import web
import sprockets.http

from app import (
    HouseholdCollectionHandler,
    HouseholdResourceHandler,
)

uuid_ = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def make_app(**settings):
    return web.Application([
        (r"/household/(?P<household_id>{u}?)/".format(u=uuid_),
            HouseholdResourceHandler),
        (r"/household/", HouseholdCollectionHandler),
    ], **settings)

if __name__ == '__main__':
    sprockets.http.run(make_app)
