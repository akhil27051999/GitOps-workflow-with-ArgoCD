# GitOps Workflow with ArgoCD 🚀☸️🎯

This project demonstrates a **complete DevOps lifecycle and GitOps workflow** using **ArgoCD**, **Kustomize**, and **Kubernetes** to deploy and manage two microservices — a **Flask API** and an **Nginx web server** — across **dev**, **staging**, and **prod** environments using the **App of Apps pattern**.

### 👨‍💻 Project Goal

To build, deploy, and manage multi-environment microservices applications in a **declarative GitOps** manner using **ArgoCD**, while following real-world **DevOps best practices**.

---

### 🛠️ DevOps Tools Stack

| Function           | Tool(s)                 |
|--------------------|--------------------------|
| Source Control     | GitHub                   |
| Containerization   | Docker                   |
| Orchestration      | Kubernetes (via kubeadm) |
| GitOps CD          | ArgoCD + Kustomize       |

---

### 🧱 Tools & Workflow Architecture

```text
                ┌────────────────────┐
                │     Developer      │
                │ Push Code to GitHub│
                └────────┬───────────┘
                         │
                         ▼
                 ┌────────────┐
                 │   GitHub   │◄────────┐
                 └────┬───────┘         │
                      │                 │
                      ▼                 │
       ┌────────────────────────┐       │
       │ ArgoCD (App of Apps)   │◄──────┘
       │ - Watches GitHub Repo  │
       │ - Auto-syncs Changes   │
       └────┬─────────┬─────────┘
            │         │
      ┌─────▼───┐ ┌───▼────┐
      │ dev env │ │ staging│
      └────┬────┘ └───┬────┘
           │          │
      ┌────▼────┐ ┌───▼────┐
      │ prod env│ │  ...   │
      └────┬────┘ └────────┘
           │
      ┌────▼────────────────────────────┐
      │  Kubernetes Cluster on EC2 VM   │
      │- Flask App Deployment & Service │
      │- Nginx Deployment & Service     │
      └─────────────────────────────────┘

```

### 📁 Repository Structure

```text

argocd-gitops-demo-project/
├── apps/                         # ArgoCD Application definitions
│   ├── app-of-apps.yaml          # Root App (manages other apps)
│   ├── dev/app.yaml              # Dev env ArgoCD App
│   ├── staging/app.yaml          # Staging env ArgoCD App
│   └── prod/app.yaml             # Prod env ArgoCD App
│
├── manifests/                    # K8s manifests
│   ├── base/                     # Common base YAMLs
│   │   ├── flask-app.yaml        # Flask Deployment & Service
│   │   └── nginx-app.yaml        # Nginx Deployment & Service
│   └── overlays/                 # Environment-specific Kustomize overlays
│       ├── dev/
│       │   └── kustomization.yaml
│       ├── staging/
│       │   └── kustomization.yaml
│       └── prod/
│           └── kustomization.yaml
└── README.md
```

## 📦 Folder-by-Folder Breakdown

### 📂 apps/

- This directory defines ArgoCD Application resources.
- app-of-apps.yaml: Root ArgoCD application that manages all child applications.
- dev/app.yaml, staging/app.yaml, prod/app.yaml: Define a K8s ArgoCD Application for each environment that points to its corresponding Kustomize overlay.

### 📂 manifests/base/

- Contains base Kubernetes manifests shared by all environments.
- flask-app.yaml: Deployment and Service for the Flask microservice.
- nginx-app.yaml: Deployment and Service for the Nginx microservice.
- These files are environment-agnostic.

### 📂 manifests/overlays/

- Environment-specific overlays using Kustomize.
- Each folder (dev/, staging/, prod/) contains a kustomization.yaml file that applies customizations like namespaces, labels, or patches on top of the base manifests.

## 🧩 Section-wise Project Overview

### ✅ Section 1: Provisioning AWS EC2 Virtual Machine and SSH Access

- Launched an EC2 instance (Ubuntu) for the deployment server.
- Configured security groups for SSH and Kubernetes ports.
- Generated SSH key pair and accessed instance securely.
- Updated system packages and installed required tools.

---

### ✅ Section 2: Installing Docker and Containerizing Applications

- Installed Docker Engine on the EC2 instance.
- Created Dockerfiles for both Flask and Nginx services.
- Built and tested the container images locally.

---

### ✅ Section 3: Setting Up Kubernetes Cluster

- Installed Kubernetes components using kubeadm.
- Configured kubeconfig for cluster management.
- Created Kubernetes namespaces: dev, staging, prod.

---

### ✅ Section 4: Writing Kubernetes Manifests

- Defined reusable Deployment and Service manifests in manifests/base/.
- These act as the shared foundation for all environments.

---

### ✅ Section 5: Environment Customization with Kustomize

- Created overlays/ directories for each environment.
- Each overlay used kustomization.yaml to customize the base manifests with:
- Environment-specific namespaces
- Labels and metadata
- Optional patches

---

### ✅ Section 6: Installing and Configuring ArgoCD

- Installed ArgoCD in the cluster under the argocd namespace.
**- Exposed the ArgoCD server using:**

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

**- Retrieved initial admin password:**

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```
- Logged into the ArgoCD web UI.

---

### ✅ Section 7: App of Apps Pattern

- Defined a root app-of-apps.yaml under apps/.
- This application points to the /apps/ directory and automatically manages child applications for all environments.

---

### ✅ Section 8: Creating ArgoCD Applications for Each Environment

- Defined app.yaml files for:
  - dev/ → points to overlays/dev/
  - staging/ → points to overlays/staging/
  - prod/ → points to overlays/prod/
    
- Enabled auto-sync and self-healing for all environments.

---

### ✅ Section 9: Sync and Deploy via ArgoCD UI
 
 - Synced the gitops-root-app from the ArgoCD UI.
 - ArgoCD automatically created and synced all environment-specific child apps.
 - Verified the following resources:
   - Deployments
   - Services
   - ReplicaSets
   - Pods

---

### ✅ Section 10: Accessing Services via Port Forwarding

**- Flask in Dev**

```bash
kubectl port-forward svc/dev-demo-app -n dev 5000:5000
```

**- Nginx in Dev**

```bash
kubectl port-forward svc/dev-nginx-app -n dev 8080:80
```
-  Replace 'dev' with 'staging' or 'prod' for other environments

## 🎉 Final Outcome

- GitOps-based deployment for dev, staging, and prod
- Kustomize overlays for clean environment separation
- ArgoCD App of Apps for scalable GitOps automation
- Real-time sync and rollback from GitHub repo

