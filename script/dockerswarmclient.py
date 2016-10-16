from docker import Client
import docker.tls as tls

#cli = Client(base_url='unix://var/run/docker.sock')
tls_config = tls.TLSConfig(  
client_cert=('/Users/kasi-mac/.docker/machine/machines/child1/cert.pem', '/Users/kasi-mac/.docker/machine/machines/child1/key.pem'),
ca_cert='/Users/kasi-mac/.docker/machine/machines/child1/ca.pem', verify=True)
cli = Client(base_url='tcp://192.168.99.101:2376', tls=tls_config)

cli.join_swarm(
  remote_addrs=['192.168.99.100:5000'], join_token='SWMTKN-1-3r6u11c6z7lye6szqvecjkcy061volsf26insp45nspclsz21d-1ustct4bq1v5b7jckgx2qizy5',
  listen_addr='192.168.99.101:5000', advertise_addr='192.168.99.101:5000'
)


####docker swarm join  --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \