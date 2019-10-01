pipeline {
    agent {
        docker {
            image 'python:3.6-alpine'
            reuseNode true
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'apt-get install mysql-server'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {

            steps {
                sh ''
                sh 'python library/manage.py test --verbose --junit-xml test-reports/results.xml library/system'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}