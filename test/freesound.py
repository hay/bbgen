import sys
sys.path.append("..")

# This example doesn't work yet
from bbgen.freesound import Freesound

fs = Freesound()
fs.query("jungle", random = True)