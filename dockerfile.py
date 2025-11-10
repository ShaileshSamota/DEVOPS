FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
stage('Build Docker Image') {
    steps {
        sh 'docker build -t flask-fitness-app:latest .'
    }
}
