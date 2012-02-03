import ldap

con = ldap.open('ldap.mit.edu')
con.simple_bind_s("", "")
dn = "dc=mit,dc=edu"
uid = "lfei"
ldap_response = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])
#fname = res[0][1]['cn'][0].split(" ")[0]
#lname = res[0][1]['cn'][0].split(" ")[-1]
#print fname
#print lname
print not ldap_response
print ldap_response
print ldap_response[0] != None
print ldap_response[0][1]['eduPersonPrimaryAffiliation'][0] != "student"
print not ldap_response or (ldap_response[0] != None and ldap_response[0][1]['eduPersonPrimaryAffiliation'][0] != "student")
