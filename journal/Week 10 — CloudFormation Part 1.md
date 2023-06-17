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
- Create the RDS Stack via CFN, this needs to be deployed first in order to connect the ECS stack to it and have the ECS services running properly.
- [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/afb5871b2998773b35bdc450fcb065d040ffbbd4) creates a new folder called db with the files template.yaml for the cfn stack and the config.toml to reference the artifacts from the deploy bucket and the parameters needed to enable cross-stack referencing from other cfn stacks.

Parameters: These are input parameters that can be customized when deploying the CloudFormation stack. The parameters include networking stack information, cluster stack information, backup retention period, RDS instance class, RDS instance identifier, database name, deletion protection, engine version, master username, and master user password.

Resources:

RDSPostgresSG: This resource creates an AWS EC2 security group for the PostgreSQL RDS instance. It allows inbound traffic on port 5432 (PostgreSQL default port) from the security group associated with the Fargate cluster.
DBSubnetGroup: This resource creates an RDS DB subnet group. It specifies the group name, description, and the subnet IDs to be associated with the RDS instance. The subnet IDs are retrieved from the imported values of the networking stack's public subnets.
Database: This is the main resource that creates the RDS PostgreSQL instance. It specifies various properties such as allocated storage, backup retention period, instance class, instance identifier, database name, subnet group, deletion protection, performance insights, engine (PostgreSQL), engine version, master username, master user password, and whether it should be publicly accessible. It also associates the RDS instance with the security group created earlier.
Outputs (currently commented out): The outputs section defines the values that will be exported from the CloudFormation stack. In this case, it seems to be exporting the cluster name, but it's currently commented out.

Overall, this CloudFormation template creates an RDS PostgreSQL database instance, sets up the necessary security groups and subnet groups, and configures various properties for the instance based on the provided parameters.

- End result should be the cloudformation template changeset deployed properly and a new RDS instance is created in AWS RDS


### 5. Create the DynamoDB Stack

##### Context:
- Create the DynamoDB Stack via SAM, SAM is mainly used for implementing deployments with serverless/lambda functions as they can package dependencies and libraries unlike CFN. 
- In this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/6bd6d60563ea6b0bcf9d1bca8ed1bf1638f33b8f#diff-370a022e48cb18faf98122794ffc5ce775b2606b09a9d1f80b71333425ec078e), the aws-sam will be installed whenever the workspace is in use.
- In this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/6bd6d60563ea6b0bcf9d1bca8ed1bf1638f33b8f#diff-b1ab1a6b3b41fe05789320a94f69d7adc956e46a30006395d431265d3e389c1e) We also added a new folder in ./aws/cfn/ddb and create a file called config.toml, added the necessary deploy variables for the s3 bucket name, region and stack name for the ddb cfn template. Parameters are also defined here as cross-referencing other variables from other cfn stacks will be used here.

- Parameters: These are input parameters that can be customized when deploying the CloudFormation stack. The parameters include the Python runtime version, memory size for the Lambda function, timeout for the function, and deletion protection flag.

Resources:

DynamoDBTable: This resource creates a DynamoDB table with the specified attributes, key schema, provisioned throughput, billing mode, and global secondary index. It also enables deletion protection based on the value of the DeletionProtectionEnabled parameter and sets the stream specification to capture new images.
ProcessDynamoDBStream: This resource creates a Lambda function using the AWS Serverless Application Model (SAM). It specifies the code location, package type, handler function, runtime, role, memory size, and timeout. The function is triggered by the DynamoDB stream from the previously created table. It processes the stream events in batches of 1 and starts from the latest record.
LambdaLogGroup: This resource creates a CloudWatch Logs log group for the Lambda function's logs. It sets the log group name and retention period.
LambdaLogStream: This resource creates a CloudWatch Logs log stream within the previously created log group. It sets the log group name and log stream name.
ExecutionRole: This resource creates an IAM role for the Lambda function. It specifies the role name, trust policy allowing Lambda to assume the role, and permissions for CloudWatch Logs, network interfaces, Lambda function invocation, and DynamoDB stream operations.

The CloudFormation template sets up a DynamoDB table, creates a Lambda function to process the table's stream, and configures the necessary IAM role and logging resources.

- Additional changes in the template are founded in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/e66631cd5f7983a8e60a25b8eaf94257b8e8b832#diff-390c3544b998cb6ea7f87d52af8ec18f16c6549110538872ff09dcf7354f3197)
- The config.toml file will be different to serve the SAM created template in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/e66631cd5f7983a8e60a25b8eaf94257b8e8b832#diff-d0a1ff02075a62655d790cb4d34a4cd570672db476eb2466e787b2c90630e951)
- Also in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/e66631cd5f7983a8e60a25b8eaf94257b8e8b832), the whole scripts for ddb deployments are restructured and put into the root path to make running the scripts easier. A **ddb-deploy** script is created and this will build the lambda (**cruddur-messaging-streams**) and package the template.yaml referenced in the file and output it in the directory which in this case is **/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml**
- End result should be a lambda function deployed AWS Lambda with the packaged code.


### 5. Create the CI/CD Stack

##### Context:
- Create the CICD Stack via CFN templates
- This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/23896a5c43320af17b13a1c21e46e0187cb4a467) emphasize on creating the template.yaml and config.toml in the respective aws/cfn/cicd folder. A deploy script is also created [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/23896a5c43320af17b13a1c21e46e0187cb4a467#diff-d345ca7b8bcc9b0f87d7f9d3fb8b4ca1017c25f5363bedff96273c3e2f4e9f60)

**- The template.yaml does this:**

Defines parameters for the GitHub branch, GitHub repository, cluster stack, service stack, and artifact bucket name.

Creates a nested CloudFormation stack (CodeBuildBakeImageStack) using the template located at nested/codebuild.yaml. This stack is responsible for building the container image used in the deployment process.
Creates an AWS CodeStar Connections connection (CodeStarConnection) for connecting to GitHub as the source provider.
Creates an AWS CodePipeline (Pipeline) with three stages: Source, Build, and Deploy.
The Source stage retrieves the application source code from the GitHub repository specified in the parameters and stores it as a code ZIP artifact in the specified artifact bucket.
The Build stage uses AWS CodeBuild to build the container image using the source code artifact from the Source stage. The CodeBuild project name is obtained from the CodeBuildBakeImageStack stack outputs.
The Deploy stage deploys the built container image to an Amazon ECS cluster and service. The cluster and service names are obtained by importing their values from the specified stack outputs (ClusterStack and ServiceStack).
Creates an IAM role (CodePipelineRole) with policies that grant necessary permissions for the CodePipeline to interact with various AWS services, including ECS, CodeStar Connections, S3, CloudFormation, and IAM itself. These policies allow actions like describing services and task definitions, updating services, using CodeStar Connections, accessing S3 buckets, and managing IAM roles and policies.
The EcsDeployPolicy grants permissions specific to ECS deployment operations.
The CodeStarPolicy grants permissions to use the CodeStar Connections connection.
The CodePipelinePolicy grants permissions required for CodePipeline operations.
The CodePipelineBuildPolicy grants permissions to start, stop, and retry CodeBuild projects.

Overall, this CloudFormation template automates the deployment process of a serverless application by setting up a CodePipeline with source code retrieval from GitHub, container image building using CodeBuild, and deployment to an ECS cluster and service.

**- While the codebuild.yaml file does this:**

The codebuild.yaml CloudFormation template sets up an AWS CodeBuild project for building container images. Here's what it does:

Defines parameters for the log group path, log stream name, CodeBuild image, compute type, timeout duration, and build specification.
Creates an AWS CodeBuild project (CodeBuild) with the specified properties:
QueuedTimeoutInMinutes: Sets the maximum number of minutes a build is allowed to be queued before it times out.
ServiceRole: Specifies the IAM role used by the CodeBuild project.
Artifacts: Defines the type of artifacts produced by the build. In this case, it is set to CODEPIPELINE since it is used in a CodePipeline.
Environment: Specifies the environment settings for the build. It includes the compute type, the CodeBuild image to use, the container type (Linux in this case), and enables privileged mode for building Docker images.
LogsConfig: Configures the logging settings for the build, including the CloudWatch Logs group, stream name, and enabling status.
Source: Defines the source type as CODEPIPELINE and specifies the build specification file to use.
Creates an IAM role (CodeBuildRole) for the CodeBuild project with the necessary policies:
ECRPolicy: Grants permissions related to Amazon Elastic Container Registry (ECR) operations, such as checking layer availability, uploading images, and retrieving images.
VPCPolicy: Grants permissions related to Amazon EC2 VPC operations, such as creating and deleting network interfaces, describing subnets and security groups, and managing network interface permissions.
Logs: Grants permissions related to AWS CloudWatch Logs operations, such as creating log groups, streams, and putting log events.
Defines an output (CodeBuildProjectName) that provides the name of the CodeBuild project created.

Overall, this template creates an AWS CodeBuild project with the specified configuration, allowing you to build container images as part of your deployment process.

- End result should have a CICD deployed in AWS Codepipeline


### 6. Create the Frontend Stack deployed in s3

##### Context:
- Deploy our Frontend in s3 instead of ECS as to save cost, this will be packaged in a cloudformation template that can help us configure it faster.
- This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/d46bfe10e713e4267901ce2433e0b100f8ce2c51) encapsulates everything that are needed to be created to execute the cloudformation frontend stack.
- config.toml is created with deploy and parameter variables indicated in the file.
- template.yaml is also created here which contains:

Parameters section defines input parameters for the template, including CertificateArn (ARN of an ACM certificate), WwwBucketName (name of the S3 bucket for the www subdomain), and RootBucketName (name of the S3 bucket for the root domain).
Resources section contains the resource definitions:
RootBucketPolicy is an AWS::S3::BucketPolicy resource that sets a bucket policy allowing public read access to objects in the root S3 bucket.
WWWBucket is an AWS::S3::Bucket resource for the www subdomain, which redirects all requests to the root domain.
RootBucket is an AWS::S3::Bucket resource for the root domain, which serves as the main bucket for hosting the static website.
RootBucketDomain and WwwBucketDomain are AWS::Route53::RecordSet resources that define DNS records for the root domain and www subdomain, respectively. They use AliasTarget to route traffic to the CloudFront distribution.
Distribution is an AWS::CloudFront::Distribution resource that sets up a CloudFront distribution for the website. It specifies the aliases (root domain and www subdomain), comment, enabled status, HTTP version, default root object, origin (S3 bucket), cache behavior, and SSL certificate.
Overall, this template creates an S3 bucket for the root domain and www subdomain, sets up DNS records using Route 53, and creates a CloudFront distribution for serving the static website content. The ACM certificate is used to enable HTTPS for the CloudFront distribution.

- Also added a deploy script for the frontend cfn stack which is similar to other scripts aside from the PATH names and naming schemes for the stack.

- End result should be an s3 bucket deployed which contain all our frontend assets. 
