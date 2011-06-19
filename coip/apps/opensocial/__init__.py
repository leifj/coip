from tastypie.api import Api
from coip.apps.opensocial.people import PersonResource, MembershipResource

opensocial_v1 = Api(api_name = "1.0")
opensocial_v1.register(PersonResource())
opensocial_v1.register(MembershipResource())