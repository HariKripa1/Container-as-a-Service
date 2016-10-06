tall GitLab:

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
* $ pip install Django

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
3. Run manage.py
      $ python manage.py runserver 7000
4. Open application through browser (Application url: localhost/ccloud )


