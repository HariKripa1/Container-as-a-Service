import subprocess
import re

output = subprocess.check_output(['/Users/kasi-mac/KasiThings/ASU/projects/Cloud Computing/Caas/script/test.sh'])
nodes=output.split('\n')
print nodes
regex = re.compile('.*PublishedPort:.*')
j = 0
for i in nodes:
    n = regex.match(i)
    #print n
    if n:
        data=n.group()
        print data
        data=data.split(':')
        port=data[1]
        print 'port: '+port
        break
        