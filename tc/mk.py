import os

for x in range(800):
    new_case = "test" + str(x) + ".xml"
    cmd = "cp test.xml " + new_case
    print "generating", new_case
    os.system(cmd) 
