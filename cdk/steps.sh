# 1. install the CDK
sudo npm install -g aws-cdk

# directory name must be cdk-app/ to go with the rest of the tutorial, changing it will cause an error
mkdir cdk-app
cd cdk-app/

# initialize the application
cdk init --language javascript

# verify it works correctly
cdk ls