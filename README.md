# Chalice Counter

Expands https://github.com/vt102/s3-static-site to include a dynamic
counter, deployed via Chalice.

## Requirements

You'll need a static site set up as https://github.com/vt102/s3-static-site.
In addition, you'll need a DynamoDB table set up with name "chalice-counter"
and a partition key of type String with name "counter".  You will need
the AWS commandline utility set up and configured correctly; see
https://aws.amazon.com/cli/ for more info.

## Deploying

```
% chalice deploy
Creating role: chalice-counter-dev
The following execution policy will be used:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "*"
      ],
      "Sid": "99079220468746708c0589ea9718cf5f"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
Would you like to continue?  [Y/n]:
Creating deployment package.
Creating lambda function: chalice-counter-dev
Initiating first time deployment.
Deploying to API Gateway stage: api
https://fejtcviaw1.execute-api.us-east-1.amazonaws.com/api/
%
```

After deploying your Lambda file, edit the index.html file in this repo
to replace the following line:

```
var count_api = 'https://fejtcviaw1.execute-api.' +
                'us-east-1.amazonaws.com/api/increment';
```

...with the URL of your API returned from `chalice deploy`.  Once
completed, upload your file to your bucket with a command such as the
following, making sure to keep it publicly readable:


```
% aws s3 cp index.html s3://counter.aws.cowell.org/ --acl public-read
upload: ./index.html to s3://counter.aws.cowell.org/index.html
%
```
