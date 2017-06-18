# alexa-tv-remote

This is a simple fun project to send commands to your TV using a standard
Alexa skill. Once created, Alexa will invoke your Lambda function, which
will interpret your response and publish the required command into an
AWS IOT topic. The Raspberry Pi (RPi) subscribes to this topic and coverts
the received messages into IR pulses for your TV to interpret.

The Alexa Skill Kit also has a Video skill, which provides a fixed set
of phrases and requires OAuth in order to bind to your device, feel free
to use this skill as a starting point if you want to go down this route!

Further improvements to this skill could be as follows:
- Improve the voice interface to make it less clunky
- Allow the user to show the EPG and scroll
- Allow the user to change the input mode (ex. HDMI1, DVI)
- Allow the user to ask for a programme, it would be expected that the
 correct channel would be found or a schedule/reminder could be set. 

_TODO: Video of the skill working_

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

### Alexa

The Alexa folder contains the skill configuration required for interacting
with the Lambda function. This skill configuration will be uploaded during
the Alexa skill creation.

### Lambda

The Lambda folder contains all the files needed to setup a Lambda 
function and the necessary IAM roles and policies needed for the service
to function correctly and make deployments easy.

### RPi

The RPi folder contains the python script which receives messages from
AWS IOT and sends them to the [LIRC](http://www.lirc.org/) daemon, 
causing an Infra-Red LED to be activated as required to send information 
to the TV.


## Getting started

### Prerequites

Git clone this repository onto your computer, you will need the files
in order to deploy them into AWS and your RaspberryPi.

`git clone https://github.com/martysweet/alexa-tv-remote.git`

### Lambda

To get started, you need an AWS account. If you don't already have one,
you can signup at https://aws.amazon.com/free. 

Once you have logged in, you will need to deploy the `resources.yaml` 
template via [Cloudformation](https://eu-west-1.console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks?filter=active)
in your desired region. In this example, we will use `eu-west-1`.

1. Create New Stack
2. Upload the `lambda/resources.yaml` file
3. Name the stack `alexa-tv-remote`
4. Click next a few times
5. Check 'I acknowledge that AWS CloudFormation might create IAM resources.'
6. Click Create

You can see the following resources which have been created by looking
at the 'Outputs' section.

![Deployed CloudFormation](screenshots/cloudformation-deployed.png)

Next, we are going to create an Access Key for our Deployment User and
setup our [AWS CLI command line tool](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)].

_TODO: Image_

Configure the Access Keys and Secret Key into a profile called `alexa-tv-remote`.

```
$ aws configure --profile alexa-tv-remote
AWS Access Key ID [None]: MYACCESSKEY
AWS Secret Access Key [None]: MYSECRETKEY
Default region name [eu-west-1]: eu-west-1
Default output format [json]: json
```


Great! Next, ensure you have the serverless framework installed by 
following [this guide](https://serverless.com/framework/docs/providers/aws/guide/installation/).

Now we can use the serverless framework to deploy our Lambda function
using the deployment user we created above. Within this project, make 
sure you are working in the `lambda` directory.

```
$ cd lambda
$ pwd
/your/dev/path/alexa-tv-remote/lambda
$ serverless deploy --stage prod
```

If that worked, you should see a Lambda function within the AWS Console.
This function will be executed by the Alexa service when triggered by 
a voice invocation.

_TODO: Image_

### AWS IOT

The next step is to setup your AWS IOT device, and download the certificates
which your RaspberryPi will use to authenticate itself with the service.

The Lambda function we setup above will use the IOT service to send messages
in real time your the RaspberryPi.

First, go to the AWS IOT service within the AWS Console.

_TODO: Image_

From here, click Create Device, and follow the steps. 

Next, attach the `alexa-tv-remote` policy to your certificate. This was
created from the CloudFormation template we deployed earlier.

### Alexa


### RPi
Deploy Cloudformation template

Create a `serverless.env.yml` file, changing the parameters to the outputs of your stack, for example:

```yaml
prod:
  DEPLOYMENT_BUCKET: 'alexa-tv-remote-deploymentbucket-1vyjbj2lfd52z'
  APPLICATION_ROLE: 'arn:aws:iam::00000000000:role/alexa-tv-remote-ApplicationRole-1WIMZC05D7HZV'
  LAMBDA_REGION: 'eu-west-1'
```

`aws configure --profile alexa-tv-remote`


`pip install AWSIoTPythonSDK`