# Infrastructure as Code avec Terraform - exécuté sur la MACHINE HÔTE (hors VM)
# Terraform se connecte au Docker de la VM Vagrant et y crée une application web.

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  # API Docker de la VM Vagrant (ouverte par Ansible sur le port 2375)
  host = "tcp://${var.vm_ip}:2375"
}

# Image téléchargée dans la VM
resource "docker_image" "nginx" {
  name         = "nginx:alpine"
  keep_locally = true
}

# Conteneur créé par Terraform
resource "docker_container" "app_terraform" {
  name  = var.container_name
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = var.external_port
  }

  restart = "unless-stopped"
}
