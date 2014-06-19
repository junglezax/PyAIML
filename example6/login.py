import sys
import json
from session import SESSION
sys.path.insert(0, "../")

if len(sys.argv) > 1:
    username = sys.argv[1]

    fpr = file('users/userList.json', 'r')
    userList = json.load(fpr)
    fpr.close()

    for u in userList:
        print u
    
    if username in userList:
       #k = SESSION.get(username)
       k._addSession(username)
       print k._sessions.keys()
    else:
       k._addSession(username)
       print k._sessions.keys()
       
       userList.append(username)

       fpr = file('users/userList.json', 'w')
       json.dump(userList, fpr)
       fpr.close()
else:
    print 'wrong usage'
