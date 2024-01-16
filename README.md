# Nginx Server with SAAS apps

This is the server side setup and configuration to host multiple applications through an
nginx reverse proxy server. All setup is in docker-compose.yml. Non-image docker setups have a Dockerfile in the related folder.

To run:
* Install Docker - choices:
   * [From documents](https://docs.docker.com/install/)
   * [From bash script](https://get.docker.com)
     * $ curl -fsSL https://get.docker.com -o install-docker.sh 
     * $ sudo sh install-docker.sh
* Enable Docker Daemon
  * $ sudo systemctl enable docker
  * $ sudo reboot now
* For https: 
  * Comment out or remove current active server listen 80
  * Uncomment server listen 80 redirect
  * Uncomment option 1 or 2 for server listen 443
  * Change proxy/website.csr to contain your website csr
  * Change proxy/website.key to contain your private key
  * Change proxy/website.pem to contain your website certificate chain
* Change proxy/default.conf file lines containing {} to your own website setup
* Run Containers:
   * sudo docker compose up -d
* Stop Containers:
   * sudo docker compose down
* List Volumes:
   * sudo docker volume ls
