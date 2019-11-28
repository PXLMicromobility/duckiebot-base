pipeline {
  agent any
  environment {
    repoName = 'duckiebot-base'
    registry = '192.168.1.5:5000'
    imageName = '$registry/$repoName:$BUILD_NUMBER'
  }
  stages {
    stage('Build') {
      steps {
        script {
          echo "{$imageName}"
        }
      }
    }
  }

}
