pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-devops-app:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/RakeshKasagani/Project_07_Sonarqube_Docker.git', branch: 'main'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar') {   // Jenkins -> Manage Jenkins -> Configure System -> SonarQube servers
                    script {
                        def scannerHome = tool 'SonarScannerCLI'   // Jenkins -> Manage Jenkins -> Tools -> SonarQube Scanner installations
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=my-devops-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://3.95.11.213:9000 \
                            -Dsonar.login=sqa_7644d5275a02c5785e54ee64174f57d864e3e625
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Deploy App') {
            steps {
                sh """
                     docker ps -q --filter "name=my-devops-app" | grep -q . && docker stop my-devops-app && docker rm my-devops-app || true
                     docker run -d --name my-devops-app -p 5000:5000 $DOCKER_IMAGE
                      """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished!"
        }
        failure {
            echo "Pipeline failed ❌"
        }
        success {
            echo "Pipeline completed successfully ✅"
        }
    }
}
