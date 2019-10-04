pipeline {
    agent any
//     {
//         docker {
//             image 'ubuntu:bionic-20190912.1'
//             reuseNode true
//         }
//     }
//     checkout([
//       $class: 'GitSCM', branches: [[name: '*/master']],
//       userRemoteConfigs: [[url: 'git@github.com:iiiiio/library_repo.git',credentialsId:'jenkinsmaster']]
//     ])
    stages {
//         stage('Build') {
//             steps {
//                 sh '/miniconda3/envs/test-travis/bin/python library/manage.py test'
//             }
//         }
        stage('Test') {
            agent {
                docker { image 'python:3.6' }
            }
            steps {
                sh 'echo skip'
                sh 'pip install -r requirements.txt'
                sh 'python library/manage.py test'
            }
        }
        stage('SonarQube Analysis') {
            agent {
                docker { image 'newtmitch/sonar-scanner:4.0.0' }
            }
            steps {

                withSonarQubeEnv(installationName: 'Online Sonar Cloud') { // If you have configured more than one global server connection, you can specify its name
//                   sh '/usr/local/Cellar/sonar-scanner/4.0.0.1744/bin/sonar-scanner'
                  sh 'sonar-scanner'
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: false
                }
                sh 'echo "skip quality gate"'
            }
        }
        stage("Deploy") {
            steps {
                sh 'git remote -v'
                sh 'git branch -a'
                sh 'git branch -d master || true'
                sh 'git fetch --all'
                sh 'git branch -a'
                sh 'git branch -vv'
                sh 'git remote show origin'
                sh 'git checkout -b master origin/master'
                sh 'git merge $GIT_BRANCH'
                sh 'git remote -v'
                withCredentials([usernamePassword(credentialsId: '36c5933e-d21f-41fe-897e-b66f619a1579', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh 'printf "%s %s" $GIT_PASSWORD $GIT_USERNAME'
                    sh 'git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/iiiiio/library_repo.git'
                }

            }
        }
    }
}

// docker run \
//   -u root \
//   --rm \
//   -d \
//   -p 8000:8080 \
//   -p 50000:50000 \
//   -v jenkins-data:/Users/Shared/Jenkins \
//   -v /var/run/docker.sock:/var/run/docker.sock \
//   jenkinsci/blueocean
//   b26a871258edf8593472579dbc9ded470d6930bf6453014fa8186eb5037919cd