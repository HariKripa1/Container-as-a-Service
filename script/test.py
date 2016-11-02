import subprocess
import re

output = subprocess.check_output(['/Users/kasi-mac/KasiThings/ASU/projects/Cloud Computing/Caas/script/test.sh'])
nodes=output.split('\n')
print nodes
regex = re.compile('Machine-Information:.*')
j = 0
for i in nodes:
    n = regex.match(i)
    if n:
        data=n.group()
        data=data.split(':')
        name=data[1]
        ip=data[2]
        instance_id=data[3]
        print name
        print ip
        print instance_id