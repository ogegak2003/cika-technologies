pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))  // Keep only last 10 builds
        timeout(time: 30, unit: 'MINUTES')             // Fail if stuck for 30 mins
        disableConcurrentBuilds()                      // Prevent parallel runs
    }
    
    environment {
        // Customizable variables
        DOCKER_IMAGE = 'ogegak2003/myapp'
        PROD_PORT = '8000'
        
        // Fixed variables (don't change these)
        VENV_PATH = 'venv'
        TEST_REPORTS = 'test-reports'
    }
    
    stages {
        stage('Prep Environment') {
            steps {
                script {
                    // Clean workspace and set display name
                    cleanWs()
                    currentBuild.displayName = "MYAPP-#${BUILD_NUMBER}"
                    
                    // Verify Docker is available
                    sh 'docker --version'
                }
            }
        }
        
        stage('Checkout & Setup') {
            steps {
                checkout scm  // Checks out your GitHub repo
                
                // Create Python virtual environment
                sh """
                    python -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Generate test reports in JUnit format
                    sh """
                        . ${VENV_PATH}/bin/activate
                        python manage.py test --noinput --verbosity=2 > ${TEST_REPORTS}/results.xml
                    """
                    
                    // Archive test results
                    junit "${TEST_REPORTS}/results.xml"
                }
            }
            post {
                always {
                    // Clean up virtual environment
                    sh "rm -rf ${VENV_PATH}"
                }
            }
        }
        
        stage('Build & Push') {
            steps {
                script {
                    // Build Docker image with commit hash tag
                    docker.build("${DOCKER_IMAGE}:${GIT_COMMIT}")
                    
                    // Push to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                        docker.image("${DOCKER_IMAGE}:${GIT_COMMIT}").push()
                        
                        // Additional push as 'latest' if on main branch
                        if (env.BRANCH_NAME == 'main') {
                            docker.image("${DOCKER_IMAGE}:${GIT_COMMIT}").push('latest')
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'  // Only deploy from main branch
            }
            steps {
                script {
                    // Manual approval step
                    timeout(time: 1, unit: 'HOURS') {
                        input(
                            message: 'Approve production deployment?',
                            parameters: [
                                string(
                                    defaultValue: '1',
                                    description: 'Scale to how many replicas?',
                                    name: 'REPLICAS'
                                )
                            ]
                        )
                    }
                    
                    // Kubernetes deployment (example)
                    withKubeConfig([credentialsId: 'kube-config']) {
                        sh """
                            kubectl set image deployment/myapp myapp=${DOCKER_IMAGE}:${GIT_COMMIT}
                            kubectl scale deployment/myapp --replicas=${REPLICAS}
                            kubectl rollout status deployment/myapp
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean workspace and archive artifacts
            cleanWs()
            archiveArtifacts artifacts: '**/staticfiles/**/*', allowEmptyArchive: true
        }
        success {
            // Send success notification
            slackSend(
                color: 'good',
                message: "SUCCESS: myapp ${GIT_COMMIT} deployed to production"
            )
        }
        failure {
            // Send failure notification
            slackSend(
                color: 'danger',
                message: "FAILED: myapp build #${BUILD_NUMBER}"
            )
        }
    }
}
