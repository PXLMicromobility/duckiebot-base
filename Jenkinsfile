pipeline {
  environment {
      repoName = 'duckiebot-base'
      registry = '192.168.1.5:5000'
      imageName = ''
    }
  agent any
  stages {
    stage('Build') {
      steps {
        sh imageName = docker.build "$registry/$repoName:$BUILD_NUMBER"
      }
    }

    stage('Push to Registry') {
      steps {
        sh docker.withRegistry(\'$registry\') {
                imageName.push() 
            }
        }
      }

    }
  }
