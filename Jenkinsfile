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

//                 sh '/usr/bin/git remote -v'
//                 sh 'git config --global credential.helper osxkeychain'
                sh 'git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"'
//                 sh '/usr/bin/git branch -a'
                sh 'git fetch --all'
                sh 'git branch -f origin/master HEAD && git checkout origin/master'
                sh 'git branch -u remotes/origin/master'
                sh 'git merge origin/$GIT_BRANCH'
//                 sh 'git remote set-url origin $GIT_URL'
//                 sh 'git push origin HEAD:master'
                sh 'git push https://iiiiio:97GAfcUz21Qw@github.com/iiiiio/library_repo.git HEAD'
            }
        }
    }
}