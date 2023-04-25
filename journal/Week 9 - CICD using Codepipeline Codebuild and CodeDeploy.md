# Week 9 — CI/CD with CodePipeline CodeBuild and CodeDeploy

#### Business Use-case
  Implement a CI/CD Pipeline with AWS Codepipeline when pull requests are created from the source repository in Github from Prod branch. 
  
  

### 1. Created a buildspec.yml file

##### Context:
  - Add a buildspec.yml file in our backend-flask directory [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/ba751839be1b3c6e30846527caac7c1e2ba2e068). This will be used by AWS Codebuild as a configuration file and it specifies the build instructions that Codebuild uses to run a build. 
  - Don't forget to change the ENV Vars in the **buildspec.yml** file in accord to your Account num etc.
  - This is divided into 3 phases: Install, Build and Post-build.

Install Phase
```sh
 install:
    runtime-versions:
      docker: 20
    commands:
      - echo "cd into $CODEBUILD_SRC_DIR/backend"
      - cd $CODEBUILD_SRC_DIR/backend-flask
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $IMAGE_URL
```

- This phase will go into the backend directory and log to ECR from there.


Build Phase
```sh
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t backend-flask .
      - "docker tag $REPO_NAME $IMAGE_URL/$REPO_NAME"
```

- The build phase will build a docker image with backend-flask as its name and this will be tagged with the repo name and image url


Post-Build Phase
```sh
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image..
      - docker push $IMAGE_URL/$REPO_NAME
      - cd $CODEBUILD_SRC_DIR
      - echo "imagedefinitions.json > [{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
      - printf "[{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
```

- The post-build phase will push the created docker image from the previous build to the ECR registry where the backend-flask image resides. Then change directory to the source directory and create an imagedefinitions.json file that specifies the image name and URI.


### 2. Create a build project in AWS Codebuild GUI


##### Context:
  - Configure AWS Codebuild and connect buildspec.yml
  
 - **Project Configuration**
  - Navigate to AWS Codebuild and create Build Project. 
  - Name your project name (In my case **cruddur-backend-flask-bake-image**)
  - Enable build badge
 
 - **Source**  
  - Source provider would be Github, **Repository in my Github Account** will be ticked.
  - Find the repository name which in my case would be **<github-username>/aws-bootcamp-cruddur-2023**  
  - Source version would be **prod** and we will create another branch from main called **prod**
 
 - **Environment**
  - Tick **managed image**
  - Environment type would be **Linux**
  - Tick **Privileged**
  - Create a new service role, this will be formed automatically **codebuild-cruddur-backend-flask-bake-image-service-role**
  - Tick **Allow AWS CodeBuild to modify...**
  - Modify Timeout for less minutes to shorten waiting times between builds
  - Leave everything else as default
  
 - **Buildspec**
  - Tick **Use a buildspec file**
  - Buildspec name will be **buildspec.yml** which is created earlier in our Github repo
  
 - **Artifacts**
  - Type will be **No artifacts**
 
 - **Cloudwatch Logs**
  - Cloudwatch logs will be created in order to debug much easier.
 
 - Create build project after the inputs from above.
 - After creating the project, I've created a policy called **CodebuildServicePolicy** and attached it to the newly created service role to allow it to access ECR permissions.
 
  
CodebuildServicePolicy
```
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:GetAuthorizationToken",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        "Resource": "*"
      }
    ]
  }  
```
 
  - Build history should return a success 

![image](https://user-images.githubusercontent.com/56792014/234263379-1ae036fa-1029-4bdf-80ce-2929ca9acc42.png)

 

### 3. Configure CodePipeline
  
  
##### Context:
  - Create a CodePipeline for our Source, Build and Deploy pipelines. This pipeline will trigger whenever a code change (e.g. pull-request, push) happens.
  
  
  - Navigate to AWS CodePipeline
  - Click **Create Pipeline**
  - Pipeline name would be **cruddur-backend-fargate**
  - Create a **New Service Role**, this will be automatically named **AWSCodePipelineServiceRole-us-east-1-cruddur-backend-fargate**
  - Artifact store would be default location 
  - Encryption key would be default 
  - Soource stage would be **Github (Version 2)**
  - Click on connect to Github with connection name as **Cruddur**
  - Select the cruddur repo which in my case **<github-username>/aws-bootcamp-cruddur-2023** 
  - Finish **Connect to Github**
  - Branch name would be prod
  - Tick **Start the pipeline on source code change**
  - Output Artifact format would be **default**
  - Variable Namespace would be **SourceVariables**
  - Output artifact would be SourceArtifact
  
 - **Build**
  - Add a stage in the CodePipeline, name it **Build**
  - Action Provider would be **AWS CodeBuild**
  - Region where most of your running services resides. (In my case US East 1)
  - Input Artifacts would be **SourceArtifact**
  - Project name would be our created build in Codebuild, mine is name **cruddur-backend-flask-bake-image**
  - Build type **single**
  - Output Artifacts will be **InputDefinitions**
 
 - **Deploy**
  - Add a stage called Deploy
  - Action provider will be **Amazon ECS**
  - Region will be the same as Build stage
  - Input Artifact will be **InputDefinitions**
  - Cluster name will be Cruddur which is created in our Amazon ECS
  - Service name will be the backend-flask
  - Everything else will be left on default

  - After setting up the Codepipeline. save the changes and release change. 
  - Everything should be running successfully after triggering a code change which in this case would be triggered only by a **pull-request** to prod branch.
  
  ![image](https://user-images.githubusercontent.com/56792014/234271615-333f646d-e987-44ba-ada5-e49e1002331f.png)

  
