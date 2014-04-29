from tastypie.resources import ModelResource
from okrs.models import Objective, KeyResult
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization

class ObjectivesResource(ModelResource):
    class Meta:
        authentication = BasicAuthentication()
        authorization = Authorization()
        queryset = Objective.objects.all()
        allowed_methods = ['get', 'post']

    def dehydrate_private(self, bundle):
        if bundle.data['private']:
            bundle.data['private'] = 'private'
        else:
            bundle.data['private'] = 'public'
        return bundle.data['private']


class KeyResultsResource(ModelResource):
    class Meta:
        queryset = KeyResult.objects.all()
        allowed_methods = ['get', 'post']