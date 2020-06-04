import os

thisvar = os.system("cd ~/padPhone/answers/" + str(5) +"&& aplay $(ls -tr | tail -1 | head -n 1)")

newString = str(thisvar)
print(newString)
