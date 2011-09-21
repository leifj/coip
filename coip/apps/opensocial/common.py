'''
Created on Sep 21, 2011

@author: leifj
'''
from tastypie.resources import ModelResource
from tastypie.bundle import Bundle
from coip.multiresponse import json_response
from django.core.serializers import json
from django.http import HttpResponseBadRequest

_rekey = {
          'objects': 'entry'
}

def system(request):
    if request.method == 'POST' and request.META['CONTENT_TYPE'] == 'application/json':
        rpc_request = json.simplejson.load(request)
        if rpc_request['method'] == 'system.listMethods':
            return json_response(['people.get','groups.get','system.listMethods'])
    else:
        return HttpResponseBadRequest()

class OpenSocialResource(ModelResource):

    def _restructure(self,request,data,depth):
        if isinstance(data, (list,tuple)):
            for v in data:
                self._restructure(request,v,depth+1)
        elif isinstance(data,dict):
            for (key,value) in data.iteritems():
                nkey = key
                if _rekey.has_key(key):
                    nkey = _rekey[key]
                
                data[nkey] = self._restructure(request,data.pop(key),depth+1)
                
            if data.has_key('meta') and depth == 1:
                meta = data.pop('meta')
                if request.GET.has_key('count'):
                    data['totalResults'] = meta['total_count']
                data['itemsPerPage'] = meta['limit']
                data['startIndex'] = meta['offset']        
        elif isinstance(data,Bundle):
            pass
        
        return data

    def alter_list_data_to_serialize(self,request,data):
        return self._restructure(request,{'response':data},0)
    
    def alter_detail_data_to_serialize(self,request,data):
        return self._restructure(request,{'response': data},0)