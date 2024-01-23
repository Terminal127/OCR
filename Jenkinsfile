pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "the127terminal"
        APP_NAME = "ocr"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${APP_NAME}" 
        REGISTRY_CREDS = 'dockerhub'
    }

    stages {
        stage('Clenup workspace') {
            steps {
                script {
                    cleanWs()
                }
            }
        }

        stage('Pull docker image') {
            steps {
                script {
                    git credentialsId: 'github',
                    url: 'https://github.com/Terminal127/OCR',
                    branch: 'main'
                }
            }
        }

        stage('Build docker image') {
            steps {
                script {
                    def lowercaseTag = "${IMAGE_TAG}".toLowerCase()
                    def dockerImageNameWithTag = "${IMAGE_NAME}:${lowercaseTag}"

                    // Change the working directory to the 'OCR' directory
                    dir('OCR') {
                        docker.withRegistry('https://registry.hub.docker.com', REGISTRY_CREDS) {
                            def customImage = docker.build(dockerImageNameWithTag)
                            customImage.push()
                        }
                    }
                }
            }
        }

        stage('Delete docker image') {
            steps {
                script {
                    def lowercaseTag = "${IMAGE_TAG}".toLowerCase()
                    def dockerImageNameWithTag = "${IMAGE_NAME}:${lowercaseTag}"

                    // Change the working directory to the 'OCR' directory
                    sh "docker rmi ${dockerImageNameWithTag}"
                    sh "docker rmi registry.hub.docker.com/the127terminal/ocr:${BUILD_NUMBER}"
                }
            }
        }
        stage('Updating the manifests') {
            steps {
                script {
                    def lowercaseTag = "${IMAGE_TAG}".toLowerCase()
                    def dockerImageNameWithTag = "${IMAGE_NAME}:${lowercaseTag}"

                    // Change the working directory to the 'OCR' directory
                    dir('manifests') {
                        sh "git checkout release"
                        sh "sed -i 's|image: ${DOCKERHUB_USERNAME}/${APP_NAME}:.*|image: ${DOCKERHUB_USERNAME}/${APP_NAME}:${IMAGE_TAG}|g' deployment.yml"


                    }
                }
            }

        }
        stage('push to repository') {
    steps {
        script {
            // Change the working directory to the 'manifests' directory
            dir('manifests') {
                sh "git config --global user.name 'Terminal127'"
                sh "git config --global user.email 'terminalishere127@gmail.com'"
                
                sh "git add deployment.yml"
                sh "git commit -m 'updated deployment.yml'"
                withCredentials([gitUsernamePassword(credentialsId: 'github')]) {
                sh "git push https://github.com/Terminal127/OCR release"
                }
            }
        }
    }
}
    

    }
}
