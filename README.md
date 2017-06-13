# alexa-tv-remote


Deploy Cloudformation template

Create a `serverless.env.yml` file, changing the parameters to the outputs of your stack, for example:

```yaml
prod:
  DEPLOYMENT_BUCKET: 'alexa-tv-remote-deploymentbucket-1vyjbj2lfd52z'
  APPLICATION_ROLE: 'arn:aws:iam::615078780108:role/alexa-tv-remote-ApplicationRole-1WIMZC05D7HZV'
  LAMBDA_REGION: 'eu-west-1'
```