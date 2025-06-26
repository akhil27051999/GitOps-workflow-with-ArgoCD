## ✅ Section 1: Provisioning AWS EC2 Virtual Machine and SSH Access

### Concept: Virtual Machines on Cloud

* **Amazon EC2** (Elastic Compute Cloud) provides resizable virtual machines in the cloud.
* Used to simulate a real deployment environment in AWS.

### Key Concepts

* **AMI (Amazon Machine Image)**: Preconfigured OS image (e.g., Ubuntu 22.04).
* **Key Pair**: SSH-based authentication mechanism for secure instance access.
* **Security Group**: Virtual firewall to allow only specific traffic (e.g., port 22 for SSH).

### Installation Rationale

* `curl`, `git`, `apt-transport-https`, `ca-certificates`: Required to install other tools securely.
* Keeping system up to date ensures compatibility and security.

### Verification & Commands

```bash
ssh -i your-key.pem ubuntu@<EC2-IP>
sudo apt update && sudo apt upgrade -y
```

### Troubleshooting

* Permission denied: `chmod 400 your-key.pem`
* Timeout: Open port 22 in Security Group.

---

## ✅ Section 2: Installing Docker and Containerizing Applications

### Concept: Containerization

* Docker packages an application and its dependencies into a single image.
* Ensures consistent behavior across all environments.

### Dockerfile Breakdown

```Dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

* **FROM**: Base image
* **WORKDIR**: Working directory inside container
* **COPY**: Copies app code
* **RUN**: Installs Python dependencies
* **CMD**: Starts the application

### Commands

```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

### Verification

* Visit `http://<EC2-IP>:5000` if exposed.

---

## ✅ Section 3: Setting Up Kubernetes Cluster (kind)

### Concept: Container Orchestration

* Kubernetes automates container deployment, scaling, and management.
* `kind` runs Kubernetes cluster in Docker (great for local/dev environments).

### Install Tools

```bash
# kind install
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# kubectl install
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

### Create Cluster

```bash
kind create cluster --name dev-cluster
kubectl cluster-info
```

---

## ✅ Section 4: Writing Kubernetes Manifests

### Concept: Infrastructure as Code (IaC)

* YAML files declare the desired state of application resources.

### Key Kubernetes Objects

* **Deployment**: Defines how to deploy and manage a ReplicaSet of Pods.
* **Service**: Exposes the app on a stable endpoint (ClusterIP or NodePort).

### Sample Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
        - name: flask-app
          image: flask-app
          ports:
            - containerPort: 5000
```

---

## ✅ Section 5: Environment Customization with Kustomize

### Concept: Declarative Overlays

* Kustomize overlays base configuration with environment-specific values (dev/staging/prod).

### Structure

```
manifests/
  base/
    deployment.yaml
  overlays/
    dev/
    staging/
    prod/
```

### kustomization.yaml

```yaml
resources:
  - ../../base
namespace: dev
commonLabels:
  env: dev
```

---

## ✅ Section 6: Installing and Configuring ArgoCD

### Concept: GitOps

* ArgoCD syncs Kubernetes resources directly from Git repositories.
* Enables continuous deployment with Git as the source of truth.

### Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Access ArgoCD

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Retrieve Admin Password

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

---

## ✅ Section 7: App of Apps Pattern

### Concept: Hierarchical GitOps Management

* One root Application manages multiple child Applications via a single manifest.
* Helps scale across multiple teams and environments.

### Sample Root App

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gitops-root-app
spec:
  source:
    repoURL: https://github.com/your/repo.git
    path: apps
    targetRevision: HEAD
  destination:
    namespace: argocd
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

---

## ✅ Section 8: ArgoCD Applications for Each Environment

### Concept: Declarative Environment Management

* Each Application manifest points to an environment overlay and is managed by ArgoCD.

### Sample Application (Dev)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-demo-app
spec:
  destination:
    namespace: dev
    server: https://kubernetes.default.svc
  source:
    repoURL: https://github.com/your/repo.git
    path: manifests/overlays/dev
    targetRevision: HEAD
  project: default
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

---

## ✅ Section 9: Sync and Deploy via ArgoCD UI

### Concept: Git-based Deployment

* ArgoCD monitors Git repos, auto-syncs changes, and applies them to K8s cluster.

### Actions

* Login to ArgoCD UI
* Click on `gitops-root-app`
* Sync the application (auto-sync and self-healing enabled)

### Verification

```bash
kubectl get pods -n dev
kubectl get svc -n dev
kubectl get deployments -n dev
```

---

## ✅ Section 10: Accessing Services via Port Forwarding

### Concept: Temporary Local Access

* `kubectl port-forward` is used to expose Kubernetes services to localhost.
* Suitable for testing in dev environments without external LoadBalancer.

### Commands

```bash
kubectl port-forward svc/dev-demo-app -n dev 5000:5000
kubectl port-forward svc/dev-nginx-app -n dev 8080:80
```

---

## 🔧 Troubleshooting Summary

| Issue                  | Cause                      | Solution                 |
| ---------------------- | -------------------------- | ------------------------ |
| SSH permission denied  | Wrong key permissions      | chmod 400 key.pem        |
| Docker command fails   | Permission issue           | Add user to docker group |
| Cluster not created    | Docker not running         | Start Docker daemon      |
| ArgoCD app not syncing | Wrong repo URL or path     | Check manifest paths     |
| Pod CrashLoopBackOff   | App issue or missing image | kubectl logs <pod-name>  |

---

## 📃 Final Commands Summary

```bash
# EC2 Setup
ssh -i your-key.pem ubuntu@<ip>
sudo apt update && sudo apt install docker.io -y

# Docker
docker build -t flask-app .
docker run -p 5000:5000 flask-app

# Kubernetes
kind create cluster
kubectl apply -k manifests/overlays/dev/

# ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d

# Access Services
kubectl port-forward svc/dev-demo-app -n dev 5000:5000
```

---

Let me know if you want the same notes exported as a README.md or PDF.
