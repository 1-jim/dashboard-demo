# Dashboard POC
Dash and Plotly in a docker container

## Configuration
Convert source files/resources to csv format and groups together to perform a single output for visualisation

## Notes
Check the requirements.txt file to ensure new dependencies are added to the docker image on build

## DEBUG
- **start docker desktop**
- **run the dockerfile to create the image**
- **compose up the yaml to create a container**
- **playtimte**

## DEPLOY
- **run the dockerfile to create your image**
- **tag the image with your registry**
- **push the image to the registry**
- **deploy as a service on port 80**