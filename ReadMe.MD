# Dashboard POC
Dash and Plotly in a docker container, includes dockerfile and compose with optional traefik labels for reverse proxy

## Configuration
Convert source files/resources to csv format and groups together to perform a single output for visualisation

## Notes
Check the requirements.txt file to ensure new dependencies are added to the docker image on build
the app requires an 'output' and a 'source' directory created. For this demo the dataset is brought into source, some basic transforms are undertaken and the output is created, then referenced by the charts.

## DEBUG
- **start docker desktop**
- **run the dockerfile to create the image**
- **compose up the yaml to create a container**
- **playtime**

## DEPLOY
- **run the dockerfile to create your image**
- **tag the image with your registry**
- **push the image to the registry**
- **deploy as a service on port 80**

deploy:
    labels:
    - traefik.enable=true
    - traefik.docker.network=traefik-public
    - traefik.constraint-label=traefik-public
    - traefik.http.routers.dash-http.rule=Host(`dash-demo.example.com`)
    - traefik.http.routers.dash-http.entrypoints=http
    - traefik.http.routers.dash-http.middlewares=https-redirect
    - traefik.http.routers.dash-https.rule=Host(`dash-demo.example.com`)
    - traefik.http.routers.dash-https.entrypoints=https
    - traefik.http.routers.dash-https.tls=true
    - traefik.http.routers.dash-https.tls.certresolver=le
    - traefik.http.services.dash.loadbalancer.server.port=8088