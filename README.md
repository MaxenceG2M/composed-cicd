# Why?

I need / want a local CI/CD for my development that run on Docker and are little.

I develop on a distant linux machine and I want to access to this CI/CD.

I want to use some cool HTTP Address than IP:PORT.

So I put a Traefik. And a DNS to resolve address.

# How to run and install

1. Start with a classic `docker-compose up -d`.
2. Create Gitea user: 
    * `docker exec -ti --user git gitea gitea --config /data/gitea/conf/app.ini  admin user create --username maxenceg2m --password maxenceg2m --email maxence@g2m.com --admin`
    * Gitea start already setted (see `gitea/gitea/conf/app.ini` file)
    * Remove this file and see "Old fashion way" to a manual install
3. Login in Gitea, add an SSH key and create an OAuth2 Application for Drone
    * Redirection: http://drone.dakota.eu/login

And heu... Everything while be alright!

# Access

* Minio : `minioadmin / minioadmin`

## DNS Error
TCP Dial Error: reboot stack (`docker-compose down && docker-compose up -d`)

## Why Technitium, an excellent but huge product?

I redirect the DNS of my desktop on Tecnhitium.
I do some test with dnsmasq, and it doesn't work after a while.
I suspect limits that I explode very quickly, where Technitium does the job

# Old fashion way
## To start
Just change hostname `edelweiss` to your hostname and run `docker-compose up -d`

## When you change hostname, do:
- Update prometheus targets configuration for drone job
- Restart prometheus services: `docker-compose restart prometheus` if stack is already up
    - --> TODO Why target with servicename doesn't work?

## The stack
> :info: You can change `localhost` by your host name in this list

- Gita: http://localhost:10050
    - Go on and install to start to use
        - Change "Server Domain" to your hostname
        - Change "SSH Server Port" to 10022
        - DON'T change "Gitea HTTP Listen Port"
        - Change "Gitea Base URL" to complete address: http://<hostname>:10050
            - Traefik: http://gitea.dakota.eu
        - DON'T FORGET to create admin user
        - Install <3
            - After install, a short redirection will fail. But after some seconds it will go on Gitea
    - While you are on Gitea, you can:
        - Add your SSH keys in your settings
        - Create drone application in "Application" section
            - ==> Create a new OAuth2 Application
            - Application name: drone
            - Redirection: http://<hostname>:8085/login
                - Traefik: http://drone.<hostname>.eu/login
        - Keep client ID and Client secret, update docker-compose with this information.
        - Save, and update stack with `docker-compose up -d`
- Drone: http://localhost:8085
    - Authorize on Github, and registry. Don't care about user name
    - Just one user by default: prometheus, for monitoring.
        - Admin right on Drone just permit to manage user. Consider as useless in the case of this stack.
- Minio: http://localhost:9001 (console: http://localhost:9000)
    - minioadmin : minioadmin
    - Create minio user:
        - drone : drone-secret
    - Check a drone-readwrie policy exist
    - TODO With multiple drive conf.
- Grafana: http://localhost:3000
    - admin : admin
    - New password? Set admin again if you want
    - Have to set a Prometheus datasource (TODO)
        - http://prometheus:9090 (use service name, same docker network)
    - import dashboard
- Prometheus: http://localhost:9090
    - Check all targets: http://localhost:9090/targets

## Push in Gitea
Add your SSH public key in Gitea account setting.
Create a repo. Add the remote to your repository. Push on this remote.
Drone should see it automatically. Enable build. Enjoy :)

## Ensure webhook is activated
Go to your Gitea repository.
Check settings -> Webhooks.
You should see an entry to '<hostname>:8085'
Sometime, first build will be a little difficulte to launch automatically. Don't hesitate to launch manually.

## Minio logs
Ensure that logs go to minio!