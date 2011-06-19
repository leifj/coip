from tastypie.api import Api
from coip.apps.api.resources import UserResource, NameResource

v1_api = Api(api_name="1.0")
v1_api.register(UserResource())
v1_api.register(NameResource())