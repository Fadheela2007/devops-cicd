# Devoir DevOps — Vagrant + Ansible + Docker + Kubernetes + Jenkins + Prometheus/Grafana + Terraform

## Architecture

```
MACHINE HÔTE (Windows)                     VM VAGRANT  Ubuntu 22.04  (192.168.56.10)
┌──────────────────────────┐               ┌──────────────────────────────────────────┐
│ VirtualBox + Vagrant     │  vagrant up   │ Ansible  → installe tout ce qui suit      │
│                          │ ────────────► │ Docker                                    │
│ Terraform (IaC)          │  tcp:2375     │  ├─ Jenkins        :8080                  │
│  └─ dossier terraform/   │ ────────────► │  ├─ Prometheus     :9090                  │
│                          │               │  ├─ Grafana        :3000                  │
│                          │               │  ├─ node-exporter  :9100                  │
│                          │               │  ├─ cAdvisor       :8082                  │
│                          │               │  └─ app-terraform  :8081 (créée par TF)   │
│                          │               │ Minikube (Kubernetes) + kubectl           │
│                          │               │  └─ demo-nginx (2 pods)                   │
└──────────────────────────┘               └──────────────────────────────────────────┘
```

- **Dans la VM** : Ubuntu Jammy 22.04, Docker, Kubernetes (Minikube), Jenkins, Prometheus, Grafana, Ansible.
- **Hors de la VM** : Terraform (Infrastructure as Code), qui pilote le Docker de la VM à distance.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `Vagrantfile` | Crée la VM Ubuntu 22.04 (6 Go RAM, 4 CPU, IP 192.168.56.10) et lance Ansible |
| `ansible/playbook.yml` | Installe Docker, kubectl, Minikube et lance Jenkins/Prometheus/Grafana |
| `ansible/files/monitoring/` | docker-compose + configuration Prometheus et Grafana |
| `k8s/demo-app.yaml` | Application nginx déployée dans Kubernetes |
| `terraform/` | Code Terraform exécuté depuis la machine hôte |

## 1. Prérequis sur la machine hôte

À installer sur l'autre machine (processeur Intel/AMD, au moins 8 Go de RAM) :

1. **VirtualBox** — https://www.virtualbox.org/wiki/Downloads
2. **Vagrant** — https://developer.hashicorp.com/vagrant/install
3. **Terraform** — https://developer.hashicorp.com/terraform/install
   (sous Windows : télécharger le .zip, extraire `terraform.exe` et ajouter son dossier au PATH)

Vérifier :
```powershell
vagrant --version
terraform --version
```

> Ansible n'a pas besoin d'être installé sur l'hôte : Vagrant l'installe automatiquement **dans** la VM.

## 2. Créer la VM et tout installer

Dans un terminal, depuis le dossier du projet :
```powershell
vagrant up
```
La première fois, ça prend **15 à 30 minutes** (téléchargement de l'image Ubuntu et des outils).
À la fin, Ansible affiche un récapitulatif avec le **mot de passe initial de Jenkins**.

## 3. Accéder aux services (depuis le navigateur de l'hôte)

| Service | Adresse | Identifiants |
|---|---|---|
| Jenkins | http://192.168.56.10:8080 | mot de passe affiché à la fin de `vagrant up` |
| Grafana | http://192.168.56.10:3000 | admin / admin |
| Prometheus | http://192.168.56.10:9090 | — |

Mot de passe Jenkins si tu l'as perdu :
```powershell
vagrant ssh -c "docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
```

**Grafana** : la source de données Prometheus est déjà configurée. Pour un tableau de bord tout prêt :
Dashboards → New → Import → saisir l'ID **1860** (Node Exporter Full) → choisir Prometheus → Import.

**Prometheus** : menu Status → Targets → les 3 cibles doivent être **UP**.

## 4. Vérifier Kubernetes (Minikube)

```powershell
vagrant ssh
```
Puis dans la VM :
```bash
minikube status
kubectl get nodes
kubectl get pods
kubectl get svc
curl $(minikube service demo-nginx --url)
```

## 5. Terraform (sur la machine hôte, hors VM)

La VM doit être allumée. Depuis le dossier du projet :
```powershell
cd terraform
terraform init
terraform plan
terraform apply
```
Taper `yes` pour confirmer. Ouvrir ensuite **http://192.168.56.10:8081** → page « Welcome to nginx! » créée par Terraform.

Supprimer ce que Terraform a créé :
```powershell
terraform destroy
```

## 6. Commandes Vagrant utiles

| Commande | Effet |
|---|---|
| `vagrant up` | Démarre la VM |
| `vagrant ssh` | Se connecte à la VM |
| `vagrant provision` | Relance Ansible |
| `vagrant halt` | Éteint la VM |
| `vagrant destroy -f` | Supprime la VM |

Après un `vagrant halt` puis `vagrant up`, relancer Minikube dans la VM : `minikube start`.

## Remarques

- Le port Docker 2375 est ouvert sans chiffrement pour que Terraform puisse atteindre la VM : c'est acceptable sur le réseau privé d'un TP, **jamais en production**.
- Si la machine a peu de RAM, baisser `vb.memory` à 4096 dans le `Vagrantfile`.
