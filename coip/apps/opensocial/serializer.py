'''
Created on Jun 19, 2011

@author: leifj
'''
from tastypie.serializers import Serializer, get_type_string
from tastypie.bundle import Bundle
from django.utils import simplejson
from django.utils.encoding import force_unicode
import string
import logging
from pprint import pformat
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers import json

try:
    import lxml
    from lxml.etree import parse as parse_xml
    from lxml.etree import Element, tostring
except ImportError:
    lxml = None

class OpenSocialSerializer(Serializer):
    
    def __init__(self, formats=None, content_types=None, datetime_formatting=None):
        super(OpenSocialSerializer,self).__init__(formats,content_types,datetime_formatting)
    
    def name_data(self,data):
        name = 'unknown'

        if hasattr(data,"resource_name"):
            name = data.resource_name()
        
        if isinstance(data,Bundle):
            name = self.name_data(data.obj)
        elif hasattr(data,"__class__"):
            name = string.lower(data.__class__.__name__)
        
        return name
    
    def to_json(self, data, options=None):
        """
        Given some Python data, produces JSON output.
        """
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data['response'], cls=json.DjangoJSONEncoder, sort_keys=True)
    
    def to_xml(self, data, options=None):
        """
        Given some Python data, produces XML output.
        """
        options = options or {}
        
        if lxml is None:
            raise ImproperlyConfigured("Usage of the XML aspects requires lxml.")
        
        etree = self.to_etree(data, options)
        etree.set("xmlns","http://ns.opensocial.org/2008/opensocial")
        
        return tostring(etree, xml_declaration=True, encoding='utf-8')
    
    def to_etree(self, data, options=None, name=None, depth=0, parent=None):
        """
        Given some data, converts that data to an ``etree.Element`` suitable
        for use in the XML output.
        """
        
        if parent is not None:
            logging.debug("+++++++++++ %d %s %s" % (depth,name,tostring(parent)))
        else:
            logging.debug("+++++++++++ %d %s <no parent>" % (depth,name))
        logging.debug(pformat(data))
        
        if parent is None:
            parent = Element(name or self.name_data(data))
        
        if isinstance(data, (list, tuple)):
            for item in data:
                element = Element(name or 'item')
                self.to_etree(item, options, depth=depth+1,parent=element)
                parent.append(element)
        elif isinstance(data, dict):
            if len(data) == 1 and depth == 0:
                for (key,value) in data.iteritems():
                    parent = self.to_etree(value, options, name=key, depth=depth+1,parent=None)
            else:
                for (key,value) in data.iteritems():
                    parent.append(self.to_etree(value, options, name=key, depth=depth+1,parent=parent))
        elif isinstance(data, Bundle):  
            element = Element(self.name_data(data))
            for field_name, field_object in data.data.items():
                self.to_etree(field_object, options, name=field_name, depth=depth+1, parent=element)
            parent.append(element)
        else:
            element = Element(name or 'value')
            simple_data = self.to_simple(data, options)
            data_type = get_type_string(simple_data)
            #if data_type != 'string':
            #    element.set('type', get_type_string(simple_data))
            if data_type != 'null':
                element.text = force_unicode(simple_data)
            parent.append(element)
        return parent