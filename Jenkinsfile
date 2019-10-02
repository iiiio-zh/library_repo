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
//                 sh 'echo "$GIT_BRANCH"'
//                 sh 'echo "GIT_LOCAL_BRANCH"'
//                 sh '/usr/bin/git pull --all'
                sh '/usr/bin/git branch -a'
                sh '/usr/bin/git remote -v'
                sh '/usr/bin/git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"'
                sh '/usr/bin/git fetch --all'
                sh '/usr/bin/git clean -f -d'
                sh '/usr/bin/git checkout origin/master'
                sh '/usr/bin/git merge origin/$GIT_BRANCH'
                sh '/usr/bin/git commit -am "deploy"'
                sh '/usr/bin/git push origin master'
            }
        }
    }
}