pipeline {
    agent any
//     {
//         docker {
//             image 'ubuntu:bionic-20190912.1'
//             reuseNode true
//         }
//     }

    stages {
//             stage("Checkout"){
//                 steps {
//                     scmVars = checkout(scm)
//                     sh 'echo "scmVars: ${scmVars}"'
//                     sh 'echo "scmVars.GIT_COMMIT: ${scmVars.GIT_COMMIT}"'
//                     sh 'echo "scmVars.GIT_BRANCH: "${scmVars.GIT_BRANCH}"'
//                 }
//             }
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
            steps {
//                 sh '/usr/bin/git remote -v'
//                 sh 'git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"'
                sh 'git branch -f origin/master HEAD && git checkout origin/master'
                sh 'git merge $GIT_BRANCH'
                sh 'git push'

            }
        }
    }
}