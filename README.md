Container as a Service - Portal to deploy and manage container
* User friendly interface for developers.
* Developers can concentrate on their application development and need not worry about deployment.
* APIs to create and manage swarm clusters, services, application deployment which can be used by THOTHLAB.

Install GitLab:

1. $ sudo apt-get install curl openssh-server ca-certificates postfix
2. $ curl -sS https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash sudo apt-get install gitlab-ce
3. $ sudo gitlab-ctl reconfigure

Clone Application from thothlab.gitlab

* git clone http://gitlab.thothlab.org/kselladu/docker.git

Install devstack:

1. Give execute permission to configDevScript.sh
      $ sudo chmod +x configDevScript.sh 
2. Run configDevScript.sh
      $ ./configDevScript.sh
Note: The script will ask you for id_rsa password: . Enter the password value “123456” or a password you can remember.
3. Run the command 
      $ ./devstack/stack.sh
4. Once the setup is complete you will be able to log into horizon via “dashboard”. Use URL: http://localhost ; username:”admin”; Password:123456.
5. Go to key-pairs under “Access and Security” and import key created in file “~/.ssh/id_rsa.pub” 
6. Modify default security group to allow ingress traffic for IPv4 – ICMP, TCP and SSH

Upgrade pip:

* $ pip install -U pip


Install Django:

* $ pip install virtualenv
* $ pip install virtualenvwrapper
* $ pip install Django
* $ pip install djangorestframework

Install RabbitMQ:

1. $ echo 'deb http://www.rabbitmq.com/debian/ testing main' |
sudo tee /etc/apt/sources.list.d/rabbitmq.list
2. $ wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc |
sudo apt-key add -	
3. $ sudo apt-get update
4. $ sudo apt-get install rabbitmq-server


Open Application

1. Go to ~/docker
      $ cd ~/docker
2. Run receive.py in background
      $ python receive.py &
2. Run receiveClusterReq.py in background
      $ python receiveClusterReq.py &
2. Run receiveDMReq.py in background
      $ python receiveDMReq.py &
2. Run receiveSwarmReq.py in background
      $ python receiveSwarmReq.py &  
3. Run manage.py
      $ python manage.py runserver 7000
4. Open application through browser (Application url: localhost/ccloud )


Files

	Path	Filename				Purpose																						New/Modified	Comments
	
	/ccloud	
	        admin.py				Django framework's file to register models													Modified	Registered model for cluster and node
			apps.py					Django framework's file to register application												Modified	Registered application
			forms.py				Django framework's file where we define all forms that will be displayed in HTML			Modified	Added forms for cluster management
			migrations				Django framework's file to store DB															Modified	DB changes
			models.py				Django framework's file to create models for database objects								Modified	Added model for cluster and node
			static					Contains CSS files																			New	
			urls.py					Django framework's file that contains URL mapping with corresponding controller's function	Modified	Mapping for cluster files
			views.py				Django framework's file that contains business logic										Modified	added controller logic for cluster management
	
	/script	
	        buildSwarmNext.sh		Shell script to build a cluster for a user who already has a cluster						New	
			buildSwarm.sh			Shell script to build first cluster for  a user												New	
			createDockerMachine.sh	Shell script to install docker machine on Nova instance created								New	
			CreateService.sh		Shell script to create service on Swarm Cluster												New	
			deleteSwarmnode.sh		Shell script to delete Swarm cluster														New	
			modifySwarm.sh			Shell script to modify Swarm cluster which will either add or delete nodes from cluster		New	
			removeService.sh		Shell script to remove a service															New	
			scaleService.sh			Shell script to scale a service																New	
    
    /templates
	        addclusterPage.html		HTML page for adding a cluster																New	
			addPage.html			HTML page for adding a service																Modified	Accepted port to deploy service
			base.html				HTML page which contains common header for all files										New	
			clusterHome.html		HTML page for showing list of clusters of a user											New	
			index.html				Index page for our application																Modified	
			login.html				Login page for our applicartion																Modified	added keystone authentication
			mainPage.html			HTML page for showing list of services of a user											Modified	
			meters.html				HTML page to show the usage statistics of a user											New	
			modifyclusterPage.html	HTML page for modifying a cluster															New	
			modifyPage.html			HTML page for modifying a service															Modified	Accepted scale as input to deploy service
			register.html			HTML page for user registration																Modified	Added openstack keystone registration
			userHome.html			HTML page to display user home 																Modified	To include cluster list in home page
    
    /ccloud_api/	
			admin.py				Django framework's file to register models													New	
			apps.py					Django framework's file to register application												New	
			migrations				Django framework's file to store DB															New	
			models.py				Django framework's file to create models for database objects								New	
			permissions.py			Django Restfulframework's file to configure permissions for user							New	
			serializers.py			Django Restfulframework's file to serialize model objects of ccloud application				New	
			views.py				Django Restfulframework's file to define business logic										New
	
	$HOME
            ccloud                  Django web application to provide docker as a service                                       Modified        
            ccloud_api              Django application that contains RESTFul APIs for cluster management                        New
            db.sqlite3              SQLite Database for our appplication                                                        Modified
            manage.py               Django framwework's configuration file                                                      Modified
            README.md               README                                                                                      Modified
            receiveClusterReq.py    Python script that listens to Cluster request queue and manages nova instances              New
            receiveDMReq.py         Python script that listens to docker machine create request queue and installs docker       New
            receive.py              Python script that listens to Service request queue and manages services                    Modified
            receiveSwarmReq.py      Python script that listens to Swarm cluster request queue and manages swarm cluster         New
            script                  Folder that contains shell script APIs                                                      New
            swarm.py                Python script that uses docker swarm python API to manage swarm cluster                     New    

	        