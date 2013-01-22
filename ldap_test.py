import ldap


# hostnames
"""
mit
umich
"""

# settings
hostname = "mit"

con = ldap.open("ldap.%s.edu" % hostname)
con.simple_bind_s("", "")
dn = "dc=%s,dc=edu" % hostname
uid = "dpetters"
res = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])
fname = res[0][1]['cn'][0].split(" ")[0]
lname = res[0][1]['cn'][0].split(" ")[-1]
print res
print fname
print lname
