pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/githubrohitsonawane7725/Predictive-Car-Price-Modelling-using-Linear-Regression-Deployed-using-AWS.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    source $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run App Test (optional)') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    echo "No tests added yet. Add pytest or similar."
                '''
            }
        }

        stage('Deploy (optional)') {
            steps {
                sh '''
                    source $VENV_DIR/bin/activate
                    nohup python app.py &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}

}

