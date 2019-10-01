pipeline {
    agent any
//     {
//         docker {
//             image 'ubuntu:bionic-20190912.1'
//             reuseNode true
//         }
//     }
    stages {
        stage('Build') {
            steps {
                sh 'python -v'
                sh 'conda activate test-travis'
                sh 'python library/manage.py testlibrary/system'
//                 sh 'apt-get update && apt-get -y install python3.6 mysql-server python3-pip'
//                 sh 'apt-get install -y libmysqlclient-dev python-dev'
//                 sh 'pip3 install -r requirements.txt'
            }
        }
//         stage('Test') {
//             steps {
//                 sh 'python3 library/manage.py testlibrary/system'
//             }
//         }
    }
}