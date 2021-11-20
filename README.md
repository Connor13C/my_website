# Server_Framework

This is the server side setup and configuration to host multiple applications through an
nginx reverse proxy server. All setup is in docker-compose.yml with a specified user for 
the current virtual machine but would need to be changed if on a different virtual machine
or operating system. Non-image docker setups have a Dockerfile in the related folder.

To run:
* Install Docker - choices:
   * [From documents](https://docs.docker.com/install/)
   * [From bash script](https://get.docker.com)
* Run Containers:
   * sudo docker-compose up -d
* Stop Containers:
   * sudo docker-compose down
* List Volumes:
   * sudo docker volume ls
