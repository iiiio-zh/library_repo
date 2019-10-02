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
//         stage('Test') {
//             steps {
//                sh '/miniconda3/envs/test-travis/bin/python library/manage.py test'
//             }
//         }
//         stage('SonarQube Analysis') {
//             steps {
//                 withSonarQubeEnv(installationName: 'Online Sonar Cloud') { // If you have configured more than one global server connection, you can specify its name
//                   sh '/usr/local/Cellar/sonar-scanner/4.0.0.1744/bin/sonar-scanner'
//                 }
//             }
//         }
//         stage("Quality Gate") {
//             steps {
//                 timeout(time: 1, unit: 'HOURS') {
//                     // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
//                     // true = set pipeline to UNSTABLE, false = don't
//                     waitForQualityGate abortPipeline: false
//                 }
//                 sh 'echo "skip quality gate"'
//             }
//         }
        stage("Deploy") {
//             environment {
//                 GIT_AUTH = credentials('76d5e510-0f74-4364-8162-e199edd00433')
//             }
            steps {
                sh 'git remote -v'
                sh 'git branch -a'
                sh 'git branch -d master || true'
//                 sh 'git config remote.origin.fetch "+refs/heads/*:refs/origin/*"'
                sh 'git fetch --all'
//                 sh 'git config credential.$GIT_URL.username iiiiio'
                sh 'git branch -a'
                sh 'git branch -vv'
                sh 'git remote show origin'
//                 sh 'git config --list'
//                 sh 'git checkout --track remotes/origin/master'
                sh 'git checkout -b master origin/master'
                sh 'git merge $GIT_BRANCH'
//                 sh 'git commit -m "deploy"'
//                 sh 'git status'
                sh 'git remote -v'
//                 sh 'git remote set-url origin git@github.com:iiiiio/library_repo.git'
//                 sh 'git push'
//              sh 'git push https://iiiiio:97GAfcUz21Qw@github.com/iiiiio/library_repo.git'
//                 sh 'printf "%s %s" $GIT_AUTH_PSW $GIT_AUTH_USR'
//                 sh 'git push https://$GIT_AUTH_USR:$GIT_AUTH_PSW@github.com/iiiiio/library_repo.git'
                withCredentials([usernamePassword(credentialsId: '76d5e510-0f74-4364-8162-e199edd00433', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
//                     sh 'printf "%s %s" $GIT_AUTH_PSW $GIT_AUTH_USR'
                    sh 'git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/iiiiio/library_repo.git'
                }

            }
        }
    }
}