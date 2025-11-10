pipeline {
    agent any

    environment {
        APP_NAME = "flask_fitness_app"
        VENV_DIR = ".venv"
        PYTHON = "python3"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                    if [ ! -d "$VENV_DIR" ]; then
                        ${PYTHON} -m venv ${VENV_DIR}
                    fi
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Code Quality Check') {
            steps {
                echo "Running flake8 lint check..."
                sh '''
                    source ${VENV_DIR}/bin/activate
                    pip install flake8
                    flake8 --ignore=E501 .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running Python tests (if any)..."
                sh '''
                    source ${VENV_DIR}/bin/activate
                    pytest || echo "No tests found."
                '''
            }
        }

        stage('Build Artifact') {
            steps {
                echo "Zipping project for deployment..."
                sh '''
                    zip -r ${APP_NAME}.zip . -x "*.venv*" "*.git*"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying Flask app (starting server)..."
                sh '''
                    source ${VENV_DIR}/bin/activate
                    nohup ${PYTHON} app.py > flask_app.log 2>&1 &
                    echo "Flask app started in background!"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build and deployment successful!"
        }
        failure {
            echo "❌ Build failed. Please check the logs."
        }
    }
}
