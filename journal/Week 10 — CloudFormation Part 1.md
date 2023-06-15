 # Week 10 — CloudFormation Part 1

#### Business Use-case
  Package used AWS Services into CloudFormation Templates, this will allow us to modify easily our AWS services configurations which are divided into different stacks.
  
  

### 1. Create the networking Stack

##### Context:
  1. This stack will contain the networking infrastructure needed for our applications to run. This will contain our VPCs, subnets, route tables, internet gateway, etc. configurations.

- This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/6039da5103ca89dbfac5601315a6a7cfd506346a) creates a new folder in our aws directory called cfn. This will contain all our created cfn stacks. The contents are as follows. Also created a bash script that will run our CFN Networking stack.

```
aws cloudformation deploy --stack-name "cruddur" \
    --template-file $CFN_PATH \
    --s3-bucket "cfn-project-artifact" \
    --no-execute-changeset
```
- This line deploys a CloudFormation stack named "cruddur" using the aws cloudformation deploy command. The stack is created based on the CloudFormation template specified by the --template-file option, which is $CFN_PATH in this case. The --s3-bucket option specifies the S3 bucket to store the CloudFormation deployment artifacts. The --no-execute-changeset option ensures that the changes are not immediately executed, allowing you to review the changes before applying them.
Overall, this script performs linting on a CloudFormation template and then deploys the stack using the template, with the option to review the changes before applying them.

CFN Stack:

Parameters: Defines the input parameters that can be passed to the template when it's deployed. In this case, the template expects parameters such as VpcCidrBlock (the CIDR block for the VPC), Az1 (availability zone 1), SubnetCidrBlocks (a comma-delimited list of CIDR blocks for subnets), Az2 (availability zone 2), and Az3 (availability zone 3).

Resources: Defines the AWS resources that will be created and configured by the template. Here, the template creates the VPC, InternetGateway (IGW), VPCGatewayAttachment to attach the IGW to the VPC, RouteTable, RouteToIGW to route traffic to the IGW, and six subnets (three public and three private).

Outputs: Specifies the values that will be returned after the stack is created, these can be cross-referenced to other stacks. The outputs include VpcId, VpcCidrBlock, SubnetCidrBlocks, SubnetIds, and AvailabilityZones.

The template creates a VPC with the specified CIDR block, enables DNS hostnames and support, and assigns a name based on the stack's name. It creates an Internet Gateway and attaches it to the VPC. The template also creates a route table and adds a default route to the Internet Gateway.

Additionally, the template creates six subnets (three public and three private) in the specified availability zones. The public subnets have the "MapPublicIpOnLaunch" property set to true, which means instances launched in those subnets will be assigned public IP addresses automatically.

- Also modified the settings.json in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/ee537ac2d750be786891674eb455332849082404) as running the bash script incurs syntax issues.

- Result should show a the CFN stack running and the resources provisioned.



### 2. Create the Cluster Stack

##### Context:
  1. This stack contains the networking for the ECS cluster and the ECS cluster resources itself for running ECS Fargate Services.

- This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/a93170e2764602082a42970671efbb5f040baa5b#diff-85801985ed8c6fb85ad7f1409f6aad37583ee9dc4fc86c7aa5264dbb96372c18) here contains the created yaml template for the provisioning of the ECS Cluster.

- Implemented a cfn-toml in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/a8310a57c1290c9eb4d5defde025466445dd6b3d#diff-abb14aad7b957b58179bd50632b68feba3238bdf0ab968c91a0eb950717109c2), the deploy scripts will be modified to accomodate the config.toml files.

Bash script that deploys a CFN stack
```
set -e #stop script execution if failed

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/config.toml"
#take a template, will name it "my-cluster", no-execute-changeset will enable us to review the changes in the template

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy --stack-name $STACK_NAME \
    --template-file $CFN_PATH \
    --region $REGION \
    --s3-bucket $BUCKET \
    --no-execute-changeset \
    --tags group=cruddur-network \
    --capabilities CAPABILITY_NAMED_IAM 
```
The bucket, region and stack name is referenced on the config.toml file.

set -e: This command enables the "exit immediately if a command exits with a non-zero status" option. In other words, if any command in the script fails (returns a non-zero exit status), the script execution will stop immediately. It ensures that any failure during the deployment process will halt the script and prevent further execution.

CFN_PATH: This variable stores the file path to the CloudFormation template (template.yaml) that will be deployed.

CONFIG_PATH: This variable stores the file path to the configuration file (config.toml) that contains deployment-related settings.

cfn-lint $CFN_PATH: This command runs a linting tool called cfn-lint on the CloudFormation template file. It checks the template for potential errors or best practice violations and provides feedback on any issues found.

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH): This command extracts the value of the deploy.bucket key from the TOML configuration file using the cfn-toml tool and assigns it to the BUCKET variable. The deploy.bucket key likely represents the name of the S3 bucket where CloudFormation artifacts will be stored.

REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH): This command extracts the value of the deploy.region key from the TOML configuration file and assigns it to the REGION variable. The deploy.region key represents the AWS region where the CloudFormation stack will be deployed.

STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH): This command extracts the value of the deploy.stack_name key from the TOML configuration file and assigns it to the STACK_NAME variable. The deploy.stack_name key represents the name of the CloudFormation stack.

PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH): This command extracts the values of the parameters defined in the TOML configuration file and assigns them to the PARAMETERS variable. The params v2 command is likely specific to the cfn-toml tool and retrieves the parameters section from the TOML file.

Finally, the aws cloudformation deploy command is used to deploy the CloudFormation stack. It specifies the stack name, template file path, region, S3 bucket, and other options like --no-execute-changeset (to review changes without executing them) and --capabilities CAPABILITY_NAMED_IAM (to acknowledge the creation of IAM resources).

- End result should be the cluster created in ECS


### 3. Create the Service Stack

##### Context:
  1. This stack contains the configuration for the running of backend services in the ECS Fargate cluster.

- This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/6cc2095385fd76f3eb5ac941fecb0b36fb1a0871#diff-370a022e48cb18faf98122794ffc5ce775b2606b09a9d1f80b71333425ec078e) will install a cfn-toml in the gitpod.yml file. This will allow us to use the config.toml files added for each Cloud Formation Stack. Also created the necessay config.toml and service deploy script.


FargateCluster: This resource creates an ECS cluster with Fargate capacity providers. It specifies the cluster name, capacity providers, and configuration options.

ALB: This resource creates an Application Load Balancer (ALB) with IPv4 support. It is an internet-facing ALB with a specified name, security groups, and subnets.

HTTPSListener: This resource creates an HTTPS listener for the ALB. It specifies the SSL certificate to be used, the default action to forward traffic to the frontend target group.

HTTPListener: This resource creates an HTTP listener for the ALB. It redirects HTTP traffic to the HTTPS listener.

ApiALBListenerRule: This resource creates a listener rule for the ALB that matches requests with the host header "api.thecloudproject.store" and forwards the traffic to the backend target group.

ALBSG: This resource creates a security group for the ALB. It allows inbound traffic on ports 443 and 80 from any IP address.

ServiceSG: This resource creates a security group for the Fargate services. It allows inbound traffic from the ALB security group on the specified backend port.

BackendTG: This resource creates a target group for the backend services. It defines the health check settings and other properties.

FrontendTG: This resource creates a target group for the frontend services. It defines the health check settings and other properties.

The Outputs section defines values that are exported for reference or use in other stacks.

The ClusterName output exports the name of the Fargate cluster.
The ServiceSecurityGroupId output exports the security group ID for the Fargate services.
The FrontendTGArn output exports the ARN (Amazon Resource Name) of the frontend target group.
The BackendTGArn output exports the ARN of the backend target group.
Overall, this CloudFormation template provisions the necessary resources to set up an ECS Fargate cluster with an ALB, target groups, and associated security groups for frontend and backend services.

- End result should be the service stack running atop of the cluster stack with a task service deployed for the backend


### 4. Create the RDS Stack

##### Context:
  - Create the RDS Stack via CFN
