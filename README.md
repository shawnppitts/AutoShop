# Auto Shop
Auto Shop app is made up of 4 microservices written in python using the flask framework:

- PortalService: The frontend of application storefront
- ProductManagement: Renders products in which we can purchase
- OrderManagement: Communicates with Mongo Database to provide productId upon purchase
- NotificationGateway: Uses Mailjet to send email when purchase is made

![image](https://github.com/shawnppitts/TheAutoShop/assets/13418953/988535ba-01f2-4f96-973c-b80e93c4a69e)

## Running in Kubernetes:
The below will create the namespace **app** with the deployments and services needed to run the application
```
$ cd kubernetes/
$ kubectl apply -f autoshop-deployment.yaml
```

To then view the application in the browser run
```
$ kubectl port-forward svc/portal 5001:5001 -n app
```

## Running locally with python:
you will need to cd into each service and run
```
$ opentelemetry-instrument python3 app.py
```

## Running Docker Compose:
To run in docker reference the following docker-compose.yaml by running
```
$ docker-compose up
```
