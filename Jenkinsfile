pipeline {
    agent any
//     {
//         docker {
//             image 'ubuntu:bionic-20190912.1'
//             reuseNode true
//         }
//     }
    stages {
//         stage('Build') {
//             steps {
//                 sh '/miniconda3/envs/test-travis/bin/python library/manage.py test'
//             }
//         }
        stage('Test') {
            steps {
               sh '/miniconda3/envs/test-travis/bin/python library/manage.py test'
            }
        }
        stage('Sonar Scan') {
            steps {
               sh '/usr/local/Cellar/sonar-scanner/4.0.0.1744/bin/sonar-scanner'
            }
        }
    }
}