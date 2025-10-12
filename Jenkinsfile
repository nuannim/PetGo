pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build & Deploy') {
      steps {
        sh 'docker compose pull || true'
        sh 'docker compose build'
        sh 'docker compose up -d --remove-orphans'
      }
    }
  }
  post {
    always {
      echo 'Pipeline finished.'
    }
  }
}