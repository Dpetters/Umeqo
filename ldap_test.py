import ldap

con = ldap.open('ldap.mit.edu')
con.simple_bind_s("", "")
dn = "dc=mit,dc=edu"
uid = "tchris"
res = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])
fname = res[0][1]['cn'][0].split(" ")[0]
lname = res[0][1]['cn'][0].split(" ")[-1]
print fname
print lname
