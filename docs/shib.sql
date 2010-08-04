
SQL for shibboleth AA resolver:

select n.display as eduPersonEntitlement from membership_membership as m, auth_user as u, name_name as n, userprofile_userprofile as p 
   where m.user_id=u.id and p.user_id=u.id and p.identifier='$identifier' 
   and m.enabled=1 and m.hidden=0 and (m.expires is NULL or m.expires < date()) and n.id=m.name_id;