pipeline {
  agent none
  stages {
    stage('Checkout') {
      agent { label 'master' }
      steps {
        sh 'hostname'
        echo 'Image to be built & pushed is "$imageName"'
      }
    }

    stage('Build') {
      agent { label 'robotnik' }
      steps {
        sh 'hostname && ls'
        sh 'docker buildx build --platform linux/arm/v7 -t "$imageName" .'
        sh 'docker push "$imageName"'
      }
    }

  }
  environment {
    repoName = 'duckietown-base'
    organization = 'pxlmicromobility'
    imageName = "$dockerHubUser/$repoName:$BUILD_NUMBER"
    registryCredential = 'DockerHub'
  }
}
