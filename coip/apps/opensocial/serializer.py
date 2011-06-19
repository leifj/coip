'''
Created on Jun 19, 2011

@author: leifj
'''
from tastypie.serializers import Serializer, get_type_string
from lxml.etree import Element
from tastypie.bundle import Bundle
from tastypie.fields import ApiField, ToOneField, ToManyField
from django.utils.encoding import force_unicode
import logging
from pprint import pformat

class OpenSocialSerializer(Serializer):
    
    def __init__(self, formats=None, content_types=None, datetime_formatting=None):
        super(OpenSocialSerializer,self).__init__(formats,content_types,datetime_formatting)
    
    def to_etree(self, data, options=None, name=None, depth=0):
        
        #logging.debug("--------")
        #logging.debug(name)
        #logging.debug(depth)
        #logging.debug(pformat(data))
        """
        Given some data, converts that data to an ``etree.Element`` suitable
        for use in the XML output.
        """

        if isinstance(data, (list, tuple)):
            element = Element(name or 'objects')
            if name:
                element = Element(name)
                #element.set('type', 'list')
            else:
                element = Element('objects')
            for item in data:
                element.append(self.to_etree(item, options, depth=depth+1))
        elif isinstance(data, dict):
            if depth == 0:
                element = Element(name or 'response',attrib={'xmlns': "http://ns.opensocial.org/2008/opensocial"} )
            else:
                element = Element(name or 'object')
                element.set('type', 'hash')
            
            if data.has_key('objects'):
                if len(data['objects']) == 1:
                    return self.to_etree(data['objects'][0], options, name=None, depth=depth)
                else:
                    for v in data['objects']:
                        element.append(self.to_etree(v, options, name='entry', depth=depth+1))
            else:
                for (key, value) in data.iteritems():
                    keyname = key
                    if keyname == 'user':
                        keyname = 'person'
                    element.append(self.to_etree(value, options, name=keyname, depth=depth+1))
        elif isinstance(data, Bundle):
            element = Element(name or 'object')
            for field_name, field_object in data.data.items():
                keyname = field_name
                if keyname == 'user':
                    keyname = 'person'
                element.append(self.to_etree(field_object, options, name=keyname, depth=depth+1))
        elif isinstance(data, ApiField):
            if isinstance(data, ToOneField):
                if data.full:
                    return self.to_etree(data.fk_resource, options, name, depth+1)
                else:
                    return self.to_etree(data.value, options, name, depth+1)
            elif isinstance(data, ToManyField):
                if data.full:
                    element = Element(name or 'objects')
                    for bundle in data.m2m_bundles:
                        element.append(self.to_etree(bundle, options, bundle.resource_name, depth+1))
                else:
                    element = Element(name or 'objects')
                    for value in data.value:
                        element.append(self.to_etree(value, options, name, depth=depth+1))
            else:
                return self.to_etree(data.value, options, name)
        else:
            element = Element(name or 'value')
            simple_data = self.to_simple(data, options)
            data_type = get_type_string(simple_data)
            if data_type != 'string':
                element.set('type', get_type_string(simple_data))
            if data_type != 'null':
                element.text = force_unicode(simple_data)
        return element