#!/bin/bash
set -e
echo "Applying manifests..."
kubectl apply -f k8s/
echo "Rolling deployment to pull :latest image..."
kubectl rollout restart deployment web
kubectl rollout status deployment web
echo "Deployed. Service URL:"
minikube service web --url
