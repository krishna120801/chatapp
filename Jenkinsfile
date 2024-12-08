pipeline{
    agent any
    enviroment{
        Docker='prod'
        kubernetes='stage'
        local='non-prod'
    }
    stages
    {
        stage("chekout"){
            checkout scm
        }
        stage("Test"){
            echo "Infra Testing...."
            sh 'python3 --version'
        }
    }
    post
    {
        failure{
            echo "There's an unexpected error, please check!"
        }
        success{
            echo "pipeline executed successfully."
        }
        always{
            echo "pipeline execution successfully completed."
        }
    }
}