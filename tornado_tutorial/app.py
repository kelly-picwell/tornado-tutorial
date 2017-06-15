import uuid
import json

from sprockets.mixins.postgresql import AsyncHandlerMixin
from tornado import gen, web
from tornado.escape import json_decode


class BaseThresholdHandler(AsyncHandlerMixin, web.RequestHandler):

    DBNAME = 'tutorial'

    def format_output(self, thresholds):
        if type(thresholds) is not list:
            thresholds['id'] = str(thresholds['id'])
        else:
            for threshold in thresholds:
                threshold['id'] = str(threshold['id'])
        return thresholds


class ThresholdCollectionHandler(BaseThresholdHandler):

    @gen.coroutine
    def post(self):
        data = json_decode(self.request.body)
        threshold_id = uuid.uuid4()
        data['id'] = threshold_id
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO threshold ( %s ) VALUES ( %s )" % (columns,
                                                              placeholders)

        result = yield self.tutorial_session.query(sql, data.values())
        result.free()
        self.finish({'data': str(threshold_id)})

    @gen.coroutine
    def get(self):
        query = 'SELECT * FROM threshold'
        result = yield self.tutorial_session.query(query)
        thresholds = self.format_output(result.items())
        result.free()
        self.finish(json.dumps(thresholds))


class ThresholdResourceHandler(BaseThresholdHandler):

    @gen.coroutine
    def get_threshold_by_uuid(self, threshold_uuid):
        threshold_id = uuid.UUID(threshold_uuid)
        query = 'SELECT * FROM threshold WHERE id = %s::uuid'
        result = yield self.tutorial_session.query(query, (threshold_id,))
        threshold = result.as_dict()
        result.free()
        raise gen.Return(self.format_output(threshold))

    @gen.coroutine
    def get(self, threshold_id):
        threshold = yield self.get_threshold_by_uuid(threshold_id)
        self.finish(json.dumps(threshold))

    @gen.coroutine
    def put(self, threshold_id):
        threshold = yield self.get_threshold_by_uuid(threshold_id)
        threshold_id = threshold.pop('id')
        data = json_decode(self.request.body)
        threshold.update(data)

        placeholders = ', '.join(['%s'] * len(threshold))
        columns = ', '.join(threshold.keys())
        threshold_id = uuid.UUID(threshold_id)
        sql = "UPDATE threshold SET ( %s ) = ( %s ) " % (columns, placeholders)
        sql_filter = "WHERE id = %s::uuid"
        values = threshold.values() + [threshold_id]
        result = yield self.tutorial_session.query(sql+sql_filter, values)
        result.free()
        self.finish(json.dumps(threshold))
