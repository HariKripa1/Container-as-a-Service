from docker import Client
import docker.tls as tls
class DockerSwarm(object):
	#path='/Users/kasi-mac/.docker/machine/machines/'
	def init_manager(self,machine_name,ip_address):
		cli = Client(base_url='unix://var/run/docker.sock')
		path='/home/ubuntu/.docker/machine/machines/'
		print path
		url='tcp://'+ip_address+':2376'
		listen_address='127.0.0.0:5000'
		tls_config = tls.TLSConfig(client_cert=(path+machine_name+'/cert.pem', path+machine_name+'/key.pem'), 
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=url, tls=tls_config)
		spec = cli.create_swarm_spec(
			snapshot_interval=5000, log_entries_for_slow_followers=1200)
		response=cli.init_swarm(
			force_new_cluster=False,
			swarm_spec=spec)
		#response='\'{u\'ID\': u\'02fn2qq2tbe07bmnxboop2iik\', u\'Version\': {u\'Index\': 11}, u\'UpdatedAt\': u\'2016-10-29T03:11:23.578188221Z\', u\'JoinTokens\': {u\'Manager\': u\'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-3cz256ilhxpz1q5066rtzsvmy\', u\'Worker\': u\'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-f07d83dxo6o3mcwzblloisljq\'}, u\'Spec\': {u\'Name\': u\'default\', u\'TaskDefaults\': {}, u\'Orchestration\': {u\'TaskHistoryRetentionLimit\': 10}, u\'Raft\': {u\'HeartbeatTick\': 1, u\'LogEntriesForSlowFollowers\': 1200, u\'ElectionTick\': 3, u\'SnapshotInterval\': 5000}, u\'CAConfig\': {u\'NodeCertExpiry\': 7776000000000000}, u\'Dispatcher\': {u\'HeartbeatPeriod\': 5000000000}}, u\'CreatedAt\': u\'2016-10-29T03:11:23.558303312Z\'}\''
		print response
		#return response
		swarm_info=cli.inspect_swarm()
		return swarm_info

	def join_swarm(self,machine_name,ip_address,master_ip,token):
		cli = Client(base_url='unix://var/run/docker.sock')
		path='/home/ubuntu/.docker/machine/machines/'
		machine_url='tcp://'+ip_address+':2376'
		listen_address=ip_address+':5000'
		remote_address=master_ip+':2377'
		tls_config = tls.TLSConfig(client_cert=(path+machine_name+'/cert.pem', path+machine_name+'/key.pem'), 
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=machine_url, tls=tls_config)
		response=cli.join_swarm(remote_addrs=[remote_address], join_token=token,listen_addr=listen_address, advertise_addr=listen_address)
  		#response='response=\'{u\'ID\': u\'02fn2qq2tbe07bmnxboop2iik\', u\'Version\': {u\'Index\': 11}, u\'UpdatedAt\': u\'2016-10-29T03:11:23.578188221Z\', u\'JoinTokens\': {u\'Manager\': u\'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-3cz256ilhxpz1q5066rtzsvmy\', u\'Worker\': u\'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-f07d83dxo6o3mcwzblloisljq\'}, u\'Spec\': {u\'Name\': u\'default\', u\'TaskDefaults\': {}, u\'Orchestration\': {u\'TaskHistoryRetentionLimit\': 10}, u\'Raft\': {u\'HeartbeatTick\': 1, u\'LogEntriesForSlowFollowers\': 1200, u\'ElectionTick\': 3, u\'SnapshotInterval\': 5000}, u\'CAConfig\': {u\'NodeCertExpiry\': 7776000000000000}, u\'Dispatcher\': {u\'HeartbeatPeriod\': 5000000000}}, u\'CreatedAt\': u\'2016-10-29T03:11:23.558303312Z\'}\''
		return response
		#swarm_info=cli.inspect_swarm()
		#print swarm_info


	def leave_swarm(self,machine_name,ip_address):
		path='/home/ubuntu/.docker/machine/machines/'
		url='tcp://'+ip_address+':2376'
		tls_config = tls.TLSConfig(client_cert=(path+machine_name+'/cert.pem', path+machine_name+'/key.pem'), 
			ca_cert=path+machine_name+'/ca.pem', verify=True)
		cli = Client(base_url=url, tls=tls_config)
		response=cli.leave_swarm(force=True)
		return response


#{u'ID': u'02fn2qq2tbe07bmnxboop2iik', u'Version': {u'Index': 11}, u'UpdatedAt': u'2016-10-29T03:11:23.578188221Z', u'JoinTokens': {u'Manager': u'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-3cz256ilhxpz1q5066rtzsvmy', u'Worker': u'SWMTKN-1-2s3ypk9js8vmzp87p47k94ygx4ovgx0r1x0yrwwzgt9ftun6ug-f07d83dxo6o3mcwzblloisljq'}, u'Spec': {u'Name': u'default', u'TaskDefaults': {}, u'Orchestration': {u'TaskHistoryRetentionLimit': 10}, u'Raft': {u'HeartbeatTick': 1, u'LogEntriesForSlowFollowers': 1200, u'ElectionTick': 3, u'SnapshotInterval': 5000}, u'CAConfig': {u'NodeCertExpiry': 7776000000000000}, u'Dispatcher': {u'HeartbeatPeriod': 5000000000}}, u'CreatedAt': u'2016-10-29T03:11:23.558303312Z'}
