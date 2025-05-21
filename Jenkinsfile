pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'forward-script-457319-a7'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'

    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/jayraj1906/hotel-reservation-prediction.git']])
                }
            }
        }

        stage('Setting up our virtual environment and installing dependencies'){
            steps{
                script{
                    echo 'Setting up our virtual environment and installing dependencies....'
                    sh '''
                    curl -Ls https://astral.sh/uv/install.sh | sh
                    export PATH=$HOME/.local/bin:$PATH
                    uv venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    uv pip install .
                    '''

                }
            }
        }

        stage('Building and pushing docker image to gcr'){
            steps{
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing docker image to gcr...'
                        sh '''
                        export PATH=$PATH:$(GCLOUD_PATH)

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:v1 .
                        docker push gcr.io/${GCP_PROJECT}/hotel-reservation-prediction:v1
                        '''
                    }
                }
            }
        }
    }
}