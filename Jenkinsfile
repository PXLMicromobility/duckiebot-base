pipeline {
  environment {
      repoName = 'duckiebot-base'
      registry = '192.168.1.5:5000'
      imageName = "$registry/$repoName:$BUILD_NUMBER"
    }
  agent any
  stages {
    stage('Build') {
      steps {
        
        sh docker.build "$imageName"
      }
    }

    stage('Push to Registry') {
      steps {
        sh docker.withRegistry('$registry') {
                imageName.push() 
            }
        }
      }
  }
}
