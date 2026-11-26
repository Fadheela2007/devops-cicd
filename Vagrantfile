# -*- mode: ruby -*-
# vi: set ft=ruby :
#
# Devoir DevOps - VM Ubuntu 22.04 (Jammy)
# Outils installés DANS la VM (par Ansible) :
#   Docker, Kubernetes (Minikube + kubectl), Jenkins, Prometheus, Grafana
# Outil installé HORS de la VM (sur la machine hôte) :
#   Terraform (Infrastructure as Code) -> voir le dossier terraform/

Vagrant.configure("2") do |config|
  # Image Ubuntu 22.04 LTS (Jammy Jellyfish)
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "devops-vm"

  # Adresse IP fixe : on accède aux services depuis la machine hôte avec cette IP
  config.vm.network "private_network", ip: "192.168.56.10"

  # Dossier du projet partagé dans la VM sous /vagrant
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |vb|
    vb.name   = "devoir-devops-vm"
    vb.memory = 6144   # 6 Go de RAM (minimum conseillé : 4096)
    vb.cpus   = 4      # Minikube a besoin d'au moins 2 CPU
  end

  # Ansible est installé automatiquement DANS la VM puis exécute le playbook
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook       = "ansible/playbook.yml"
    ansible.install        = true
    ansible.install_mode   = "default"
    ansible.compatibility_mode = "2.0"
  end
end
