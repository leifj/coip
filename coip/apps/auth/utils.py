'''
Created on Jul 7, 2010

@author: leifj
'''
from uuid import uuid4

def nonce():
    return uuid4().hex;

def anonid():
    return uuid4().urn;