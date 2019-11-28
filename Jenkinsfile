pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        script {
          sh docker.build "$imageName"
        }

      }
    }

    stage('Push to Registry') {
      steps {
        script {
          sh docker.withRegistry('$registry') {
            imageName.push()
          }

        }

      }
    }

  }
  environment {
    repoName = 'duckiebot-base'
    registry = '192.168.1.5:5000'
    imageName = "$registry/$repoName:$BUILD_NUMBER"
  }
}