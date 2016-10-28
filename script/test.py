import subprocess
import re

output = subprocess.check_output(['/Users/kasi-mac/KasiThings/ASU/projects/Cloud Computing/Caas/script/test.sh'])
print output
regex = re.compile('Machine-Information:.*')
print regex
outputs = output.split('\n')
print outputs
for line in outputs:
	match = regex.match(line)
	if match:
		data=match.group()
		data=data.split(':')
		print 'Name: '+data[1]
		print 'IP Address: '+data[2]