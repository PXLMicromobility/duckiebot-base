pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        script {
          echo "{$imageName}"
          sh docker.build ("$imageName")
          sh docker.push()
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
