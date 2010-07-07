'''
Created on Jul 7, 2010

@author: leifj
'''
from coip.apps.name.models import Name

#TODO implement acls
def has_permission_name(user,name,perm):
    return True

def has_permission(user, object, perm):
    if type(object) == Name:
        return has_permission_name(user,object,perm)
    
    return False;