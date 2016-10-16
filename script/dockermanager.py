from docker import Client
import docker.tls as tls

#cli = Client(base_url='unix://var/run/docker.sock')
tls_config = tls.TLSConfig(  
client_cert=('/Users/kasi-mac/.docker/machine/machines/default/cert.pem', '/Users/kasi-mac/.docker/machine/machines/default/key.pem'),
ca_cert='/Users/kasi-mac/.docker/machine/machines/default/ca.pem', verify=True)
cli = Client(base_url='tcp://192.168.99.100:2376', tls=tls_config)

spec = cli.create_swarm_spec(
  snapshot_interval=5000, log_entries_for_slow_followers=1200
)
response=cli.init_swarm(
  advertise_addr='192.168.99.100', listen_addr='0.0.0.0:5000', force_new_cluster=False,
  swarm_spec=spec
)
print response
swarm_info=cli.inspect_swarm()
print swarm_info



