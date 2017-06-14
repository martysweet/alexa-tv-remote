# alexa-tv-remote

Todo: What this project is


## Finding your way round

Below is a breakdown of the folders and files of this project, each is explained more within
this README.md file.

```
alexa
 - ask.json (Intent document for the Alexa skill configuration)
lambda
 - lambda.py (Lambda Skill which is invoked by the Alexa Skill Service)
 - resources.yaml (CloudFormation template to setup deployment resources and IOT policies)
 - serverless.yml (Serverless Framework configuration for deploying the Lambda function)
 - serverless.env.yml (Serverless Framework environmental file, you will need to edit this file)
rpi
 - rpi.py (RPI python script, you will need LIRC and AWSIoTPythonSDK to use this)
```


Deploy Cloudformation template

Create a `serverless.env.yml` file, changing the parameters to the outputs of your stack, for example:

```yaml
prod:
  DEPLOYMENT_BUCKET: 'alexa-tv-remote-deploymentbucket-1vyjbj2lfd52z'
  APPLICATION_ROLE: 'arn:aws:iam::615078780108:role/alexa-tv-remote-ApplicationRole-1WIMZC05D7HZV'
  LAMBDA_REGION: 'eu-west-1'
```

`aws configure --profile alexa-tv-remote`


`pip install AWSIoTPythonSDK`