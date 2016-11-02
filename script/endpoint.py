import six
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
	for k, v in dict.iteritems(ports):
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
	return result
