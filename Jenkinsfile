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
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv() { // If you have configured more than one global server connection, you can specify its name
                  sh '/usr/local/Cellar/sonar-scanner/4.0.0.1744/bin/sonar-scanner'
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}