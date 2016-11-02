from docker import Client
import docker.tls as tls
tls_config = tls.TLSConfig(  
client_cert=('/Users/kasi-mac/.docker/machine/machines/default/cert.pem', '/Users/kasi-mac/.docker/machine/machines/default/key.pem'),
ca_cert='/Users/kasi-mac/.docker/machine/machines/default/ca.pem', verify=True)
cli = Client(base_url='tcp://192.168.99.100:2376', tls=tls_config)
t=cli.login(username='dockertestme',password='pozx1230_')
for line in cli.pull('dockertestme/js1', stream=True):
	print(json.dumps(json.loads(line), indent=4))
response = [line for line in cli.push('dockertestme/ubun', stream=True)]
#pozx1230_ dockertestme
container_spec = docker.types.ContainerSpec(image='dockertestme/js1')
task_tmpl = docker.types.TaskTemplate(container_spec)
test_impl={'Spec':{'Ports':[{'Protocol': 'tcp', 'PublishedPort': '8080', 'TargetPort': '8080'}]}}
service_id = cli.create_service(task_tmpl, name='api_test',endpoint_spec=cli.create_endpoint_config(test))
test_impl= {"Spec": {"Mode": "vip", "Ports": [{"Protocol": "tcp", "TargetPort": 80, "PublishedPort": 8080 } ] }, "Ports": [{"Protocol": "tcp", "TargetPort": 80, "PublishedPort": 8080 } ], "VirtualIPs": [{"NetworkID": "birxf7xheysw1z8z80xu4uk9p", "Addr": "10.255.0.4/16"} ] }

t=endpoint.EndpointSpec(mode='vip',ports={8081:8080})

test={'Spec': t }


ports={8080:8080}


sudo docker --tlsverify --tlscacert=/home/ubuntu/.certs/ca.pem --tlscert=/home/ubuntu/.certs/cert.pem --tlskey=/home/ubuntu/.certs/key.pem -H swarm:3376 version




container_spec = docker.types.ContainerSpec('busybox', ['true'])
task_tmpl = docker.types.TaskTemplate(container_spec)
name = self.get_service_name()
endpoint_spec = endpoint.EndpointSpec(ports={12357: (1990, 'udp'),12562: (678,),53243: 8080,})
svc_id = cli.create_service(task_tmpl, name=name, endpoint_spec=endpoint_spec)




host_config=cli.create_host_config(publish_all_ports= True)

{'Ports': [
                    {
                        'Protocol': 'tcp',
                        'TargetPort': 80,
                        'PublishedPort': 8080
                    }
                ]
}

import swarm
test=swarm.DockerSwarm()
test.init_manager('default','192.168.99.100')
test.leave_swarm('default','192.168.99.100')

docker service create --replicas 1 --name service_1 dockertestme/ubun


docker --tlsverify --tlscacert=/Users/kasi-mac/.docker/machine/machines/default/ca.pem --tlscert=/Users/kasi-mac/.docker/machine/machines/default/cert.pem --tlskey=/Users/kasi-mac/.docker/machine/machines/default/key.pem -H 192.168.99.100:2376 create --replicas 1 --name service_1 dockertestme/js1

class EndpointSpec(dict):
	def __init__(self, mode=None, ports=None):
		if ports:
	    	self['Ports'] = convert_service_ports(ports)
		if mode:
	    	self['Mode'] = mode


	def convert_service_ports(ports):
		if isinstance(ports, list):
	    	return ports
		if not isinstance(ports, dict):
	    	raise TypeError(
	        	'Invalid type for ports, expected dict or list'
	    	)

		result = []
		for k, v in six.iteritems(ports):
	    	port_spec = {
	        	'Protocol': 'tcp',
	        	'PublishedPort': k
	    	}

	    	if isinstance(v, tuple):
	        	port_spec['TargetPort'] = v[0]
	        	if len(v) == 2:
	            	port_spec['Protocol'] = v[1]
	    	else:
	        	port_spec['TargetPort'] = v

	    	result.append(port_spec)
	    	print result
		return result