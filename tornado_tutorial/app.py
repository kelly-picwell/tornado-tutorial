import uuid
from tornado import gen, web
from tornado.escape import json_decode
from sprockets.mixins.postgresql import AsyncHandlerMixin


class BaseHouseholdHandler(AsyncHandlerMixin, web.RequestHandler):
   DBNAME = 'tutorial'

   def format_output(self, households):
       for household in households:
           household['id'] = str(household['id'])
       return households


class HouseholdCollectionHandler(BaseHouseholdHandler):

   @gen.coroutine
   def get(self, *args, **kwargs):
       result = yield self.tutorial_session.query('SELECT * FROM household')
       households = self.format_output(result.items())
       self.finish({'data': households})
       result.free()

   @gen.coroutine
   def post(self, *args, **kwargs):
       data = json_decode(self.request.body)
       household_id = uuid.uuid4()
       query = """INSERT INTO household (id, external_id, income, zip_code_3,
                  client_name) VALUES (%s, %s, %s, %s, %s)"""
       result = yield self.tutorial_session.query(query,
                                                 (household_id, data['external_id'],
                                                  data['income'], data['zip_code_3'],
                                                  data['client_name']))
       self.finish({'data': str(household_id)})
       result.free()


class HouseholdResourceHandler(BaseHouseholdHandler):

    @gen.coroutine
    def get(self, household_id, *args, **kwargs):
        household_id = uuid.UUID(household_id)
        query = 'SELECT * FROM household WHERE id = %s::uuid'
        result = yield self.tutorial_session.query(query, (household_id,))
        households = self.format_output(result.items())
        self.finish({'data': households})
        result.free()
