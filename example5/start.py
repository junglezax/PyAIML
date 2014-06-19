import sys
import atexit
sys.path.insert(0, "../")
import shelve

import aiml


db = shelve.open("session.db", "c", writeback=True)

atexit.register(lambda : k.saveBrain('brain.sav'))

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel(sessionStore=db)

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("cn-startup.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml cn")


# Loop forever, reading user input from the command
# line and printing responses.
while True:
    t = raw_input("> ")
    if t == 'bye':
        break
    else:
        print k.respond(t)
        db.sync()