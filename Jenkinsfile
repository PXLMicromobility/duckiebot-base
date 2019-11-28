pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo "$imageName"
        sh 'docker build -t "$imageName" .'
      }
    }

  }
  environment {
    repoName = 'duckietown-base'
    registry = '192.168.1.5:5000'
    imageName = "$registry/$repoName:$BUILD_NUMBER"
  }
}
