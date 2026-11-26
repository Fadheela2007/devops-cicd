pipeline {
    agent any

    // Jenkins interroge Git toutes les 2 minutes et lance un build si le code a change
    triggers { pollSCM('H/2 * * * *') }

    options { disableConcurrentBuilds() }

    environment {
        KUBECONFIG = '/var/jenkins_home/kubeconfig'
        IMAGE      = "mon-app:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Tests') {
            steps { sh 'docker build --target test -t mon-app:test app' }
        }
        stage('Conteneurisation') {
            steps { sh 'docker build --target final -t "$IMAGE" app' }
        }
        stage('Chargement dans Minikube') {
            steps {
                sh '''
                    if docker exec minikube docker info >/dev/null 2>&1; then
                        docker save "$IMAGE" | docker exec -i minikube docker load
                    else
                        docker save "$IMAGE" | docker exec -i minikube ctr -n k8s.io images import -
                    fi
                '''
            }
        }
        stage('Deploiement Kubernetes') {
            steps {
                sh 'sed "s/IMAGE_TAG/$BUILD_NUMBER/g" k8s/mon-app.yaml | kubectl apply -f -'
                sh 'kubectl rollout status deployment/mon-app --timeout=180s'
            }
        }
        stage('Verification') {
            steps { sh 'curl --fail --retry 10 --retry-delay 3 --retry-all-errors http://minikube:30081/health' }
        }
    }

    post {
        success { echo "Version ${env.BUILD_NUMBER} en ligne : http://192.168.56.10:8083" }
        failure { echo 'Echec : lire la premiere etape en rouge dans la sortie console.' }
    }
}
