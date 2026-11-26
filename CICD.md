# Partie CI/CD : Jenkins, Kubernetes, Prometheus, Grafana

    git push -> GitHub -> Jenkins -> tests -> image Docker -> Minikube
                                                                 |
                                     Prometheus (metriques) -----+--> Grafana

Les anciennes instructions restent dans `README.md`.

## Ce que tu dois faire

### 1. Mettre le dossier sur GitHub (depuis cette machine)
Creer un depot **public et vide**, puis dans PowerShell, dans le dossier du projet :

    git init -b main
    git add .
    git status          # .vagrant et terraform.tfstate ne doivent PAS apparaitre
    git commit -m "Projet DevOps avec CI/CD Jenkins"
    git remote add origin https://github.com/TON-COMPTE/TON-DEPOT.git
    git push -u origin main

(Si le dossier est deja un depot Git : seulement `git add .`, `git commit`, `git push`.)

### 2. Sur l'autre machine
Installer VirtualBox, Vagrant et Git (8 Go de RAM minimum, 12 Go conseilles, virtualisation activee), puis :

    git clone https://github.com/TON-COMPTE/TON-DEPOT.git
    cd TON-DEPOT
    vagrant up

Ne pas copier le dossier `.vagrant` d'une machine a l'autre.
La premiere fois : 20 a 40 minutes. En cas d'erreur reseau : `vagrant provision`.

### 3. Configurer Jenkins (http://192.168.56.10:8080)
1. Coller le mot de passe affiche a la fin de `vagrant up`.
2. Installer les plugins suggeres, creer le compte administrateur.
3. Nouveau Item > `mon-app` > **Pipeline**.
4. Definition : **Pipeline script from SCM** > **Git** > URL du depot > branche `*/main` > Script Path `Jenkinsfile`.
5. Sauvegarder puis **Lancer un build** (obligatoire la premiere fois).

Application : http://192.168.56.10:8083

### 4. Demontrer le CI/CD
Changer `MESSAGE` dans `app/app.py`, puis `git add app/app.py`, `git commit -m "Nouveau message"`, `git push`.
Jenkins lance un build en 2 minutes maximum, sans clic.

### 5. Demontrer l'observabilite
- Prometheus http://192.168.56.10:9090 > Status > Targets : `mon-app` doit etre **UP** (DOWN est normal avant le premier build).
- Grafana http://192.168.56.10:3000 > Dashboards > **Mon application**.
- Creer du trafic (PowerShell) :

      1..200 | % { curl.exe -s http://192.168.56.10:8083/ > $null; Start-Sleep -Milliseconds 300 }

- Ouvrir http://192.168.56.10:8083/erreur pour faire apparaitre des erreurs 500.

## Apres un redemarrage de la VM

    vagrant up
    vagrant ssh -c "minikube start"

## Limites (TP uniquement)
Jenkins pilote le Docker de la VM et a les droits administrateur sur Kubernetes. Ne pas exposer sur Internet.
