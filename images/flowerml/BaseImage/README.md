# NCT-TSO-BaseDocker
This folder contains the base docker setup for various challenges and frameworks hosted by the TSO group of the NCT Dresden.
It allows to run python code and pytorch models in a docker container.

# How to Kubernetes
For some projects it is necessary to run code in a Kubernetes cluster.
Kubernetes provides a platform for managing and orchestrating containerized applications.
We are able to deploy, scale and manage applications across a distributed cluster of nodes.

This folder contains a sample setup for a Kubernetes cluster.

## 1. Install Kubernetes

Prerequisites:
- [Docker](https://docs.docker.com/install/) 
- or
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

Installation:
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

## 2. Start Kubernetes Cluster 

Start Minikube:
```bash
export HTTP_PROXY=http://ukd-proxy:80
export HTTPS_PROXY=http://ukd-proxy:80
export NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.59.0/24,192.168.49.0/24,192.168.39.0/24

minikube start --driver=virtualbox --docker-env HTTP_PROXY=$HTTP_PROXY --docker-env HTTPS_PROXY=$HTTPS_PROXY
```

Mount Volumes:
```bash
minikube mount /mnt/ceph/:/mnt/ceph/
```

## 3. Start Container

```bash
kubectl apply -f deployment.yaml
```
