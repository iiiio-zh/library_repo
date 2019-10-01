pipeline {
    agent {
        docker {
            image 'bionic-20190912.1'
            reuseNode true
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'sudo apt-get update && sudo apt-get install python3.6'
                sh 'sudo apt-get install mysql-server'
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