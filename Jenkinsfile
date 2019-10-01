pipeline {
    agent {
        docker {
            image 'ubuntu:bionic-20190912.1'
            reuseNode true
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'apt-get update && apt-get -y install python3.6 && apt-get install -y mysql-server && apt-get install -y python3-pip'
                sh 'pip3 install -r requirements.txt'
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