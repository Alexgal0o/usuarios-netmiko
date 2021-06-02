users ="""username cisco secret 5 $1$nBpI$Q23CIhNWj4nUp2wAH5sY9.
username david secret 5 $1$O5H3$d9vo6dcC6X7PASBbRL63//
username abi secret 5 $1$q8f1$c5kHLDhU2PsL9lBNoHCxI/
"""

#users = [user.split()[1],user.split()[2] for user in iter(users.splitlines())]

#print(users)
for user in users.splitlines():
    print(user.split()[1])