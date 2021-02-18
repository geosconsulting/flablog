from app import api
from flask_restful import Resource
from sqlalchemy.orm import scoped_session , sessionmaker

from app.models import sparc_engine

from app.models import User, users_schema, user_schema
from app.models import Flood, floods_schema, flood_schema
from app.models import EmdatFlood,floods_emdat_schema

db_session = scoped_session(sessionmaker(bind=sparc_engine))

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

api.add_resource(UserListResource, '/users')

class UserSingleResource(Resource):
    def get(self,id):
        """
               Return FlaskRESTful Resource
               It works also with swag_from, schemas and spec_dict
               ---
               parameters:
                 - in: path
                   name: id
                   type: integer
                   required: false
               responses:
                 200:
                   description: A single user item
                   schema:
                     id: id
                     properties:
                       username:
                         type: integer
                         description: The id of the user
                         default: 1
                """
        user = User.query.get_or_404(id)
        return user_schema.dump(user)

api.add_resource(UserSingleResource, '/user/<id>')

class FloodListResource(Resource):
    def get(self):
        floods = db_session.query(Flood).all()
        return floods_schema.dump(floods)

api.add_resource(FloodListResource, '/floods_sparc')

class FloodListCountryResource(Resource):
    def get(self,iso):
        """
                    SPARC - People by Flood
                    It works also with swag_from, schemas and spec_dict
                    ---
                    parameters:
                        - in: path
                          name: iso
                          type: string
                          required: true
                    responses:
                        200:
                            description: People By Flood Probability
                            schema:
                                iso: iso
                                properties:
                                    username:
                                        type: integer
                                        description: The id of the user
                                        default: 1
                """
        floods_country = db_session.query(Flood).filter(Flood.iso3 == iso).all()
        return floods_schema.dump(floods_country)

api.add_resource(FloodListCountryResource, '/floods_sparc/<string:iso>')

class FloodsEmdatResource(Resource):
    def get(self):
        floods_emdat = db_session.query(EmdatFlood).all()
        return floods_emdat_schema.dump(floods_emdat)

api.add_resource(FloodsEmdatResource, '/floods_emdat')

class FloodsEmdatCountryResource(Resource):
    def get(self,country):
        """
                            EMDAT - Historical Floods
                            ---
                            parameters:
                                - in: path
                                  name: country
                                  type: string
                                  required: true
                            responses:
                                200:
                                    description: Historical Floods registered in the EMDATA Database
                                    schema:
                                        country: country
                                        properties:
                                            username:
                                                type: integer
                                                description: The id of the user
                                                default: 1
                        """
        floods_country = db_session.query(EmdatFlood).filter(EmdatFlood.country == country).all()
        return floods_emdat_schema.dump(floods_country)

api.add_resource(FloodsEmdatCountryResource, '/floods_emdat/<string:country>')




