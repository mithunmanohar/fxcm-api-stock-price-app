import os
import sys
try:
    sys.path.append(os.getcwd())
except Exception as e:
    print "EXCEPTION: Error in inserting python path"