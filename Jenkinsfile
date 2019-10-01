pipeline {
    properties([pipelineTriggers([githubPush()])]
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.6-alpine'
                }
            }
            steps {
                sh 'python -m py_compile library'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.6-alpine'
                }
            }
            steps {
                sh 'python manage.py test --verbose --junit-xml test-reports/results.xml library/system'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}