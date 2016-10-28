from docker import Client
import docker.tls as tls
class DockerSwarm(object):
	#path='/Users/kasi-mac/.docker/machine/machines/'
	def init_manager(self,machine_name,ip_address):
		cli = Client(base_url='unix://var/run/docker.sock')
		path='/Users/kasi-mac/.docker/machine/machines/'
		url='tcp://'+ip_address+':2376'
		listen_address='0.0.0.0:5000'
		tls_config = tls.TLSConfig(client_cert=(path+machine_name+'/cert.pem', path+machine_name+'/key.pem'), 
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=url, tls=tls_config)
		spec = cli.create_swarm_spec(
			snapshot_interval=5000, log_entries_for_slow_followers=1200)
		response=cli.init_swarm(
			advertise_addr=ip_address, listen_addr=listen_address, force_new_cluster=False,
			swarm_spec=spec)
		print response
		swarm_info=cli.inspect_swarm()
		print swarm_info

	def join_swarm(self,machine_name,ip_address,master_ip,token):
		cli = Client(base_url='unix://var/run/docker.sock')
		path='/Users/kasi-mac/.docker/machine/machines/'
		machine_url='tcp://'+ip_address+':2376'
		listen_address=ip_address+':5000'
		remote_address=master_ip+':5000'
		tls_config = tls.TLSConfig(  
		client_cert=(path+machine_name+'/cert.pem', 
			path+machine_name+'/key.pem'),
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=machine_url, tls=tls_config)
		response=cli.join_swarm(
  			remote_addrs=[remote_address], join_token=token,
  			listen_addr=listen_address, advertise_addr=listen_address)
		print response
		swarm_info=cli.inspect_swarm()
		print swarm_info


	def leave_swarm(self,machine_name,ip_address):
		path='/Users/kasi-mac/.docker/machine/machines/'
		url='tcp://'+ip_address+':2376'
		tls_config = tls.TLSConfig(client_cert=(path+machine_name+'/cert.pem', path+machine_name+'/key.pem'), 
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=url, tls=tls_config)
		response=cli.leave_swarm(force=True)
		print response










