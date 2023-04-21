# Week 8 — Serverless Image Processing

#### Business Use-case
 Deploy a Serverless Image Processing with the use of AWS CDK. CDKs allows us to deploy self contained functions that run in response to events or requests which in this case would be the image files to be uploaded for our Avatar's Profile. Leveraging serverless CDKs allows us to avoid the management and provisioning of the underlying compute by entrusting its management to the cloud provides, as well as incurring less cost as we are only charged for the actual usage of the functions created in the CDKs rather than the capacity of the infrastructures. 



### 1. Implement CDK Stack

##### Context:
  - Created a **thumbing-serverless-cdk** in root directory.
  - Run the command 
 
```sh
npm install aws-cdk -g
```
  - In this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/881aa5ec4fb34f0b6d5c0a221824dee616a3aa57#diff-370a022e48cb18faf98122794ffc5ce775b2606b09a9d1f80b71333425ec078e), the necessary CDK stack code is created.

  - We'll also need to create the s3 buckets to where the uploaded images will be sent for CDK. The s3 bucket should be named relevant to its use-case, mine will be **assets.thecloudproject.store**, another s3 bucket will be created by the CDK called  `thecloudproject-uploaded-avatars` which is from the env vars `UPLOADS_BUCKET_NAME`.
  
  - We'll be creating a lambda function which will process our images to the right format [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-40d8b09d181ff1a7d3c1b1f69f06d6015e074bf996803cd409c532548a43bd9c) , and another lambda function for the upload of the image to our s3 bucket in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-849622b4b242ea3541407533ac2cdb116ec10fbf6e1d6d556feb5944eb532299)  

  - This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/c2578a46b56b13073c663c915b9036169dc78708#diff-3a26f6bb4f45339b6822d778cdb41d2ff72716636966a7a43c48a6b0a057307f) shows env files created for the CDK stack contents such as the `UPLOADS_BUCKET_NAME` & `ASSETS_BUCKET_NAME`.

  - We've also need to install sharp to our aws/lambdas/process-images

```sh
npm install
rm -rf node_modules/sharp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install --arch=x64 --platform=linux --libc=glibc sharp
```

  - Bash scripts are created to automate these npm installs [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-0f12026649ff29f63cd9ff1a7ea11489c80a321fcb665f055d0983990cb619a6)

  - Testing of files uploaded to s3 are created as bash scripts [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-342b82f9713e6f09592c0103d336d9370a766105ae067ae6be17f81e21c1a408) run them as `./bin/avatar/upload`
 
  - Deleting those files also has a bash script to hasten the testing [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-a715a421a7bf4283e6bffca08cffd4bf3bb1b221d95525ec78d854b75cb343c5)
 
  - We will also add an S3 Event notification to SNS and to Lambda as well as a Policy for Bucket Access, the policies will be attached to the lambda role created. [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/7c8093558cb5d8fbfd3309a95c0af397d8cf672f#diff-6be534b5f75d78dfcb7e3e037c1d79a5012aa2c034e836b0b90e048fce60b831)
 
  - To create the CDK Stack in CloudFormation, these commands will be ran

```sh
cdk deploy
```
  - Result should show the CDK stack being created in the CloudFormation section of AWS Console.
  - The uploaded image file which is called `data.jpg` should be uploaded to the `thecloudproject-uploaded-avatars` s3 bucket and the image processing Lambda function will process the uploaded image and saves it in the avatars folder of my `assets.thecloudproject.store`.

### 2. Serve Avatars via CloudFront

##### Context:
  - We have to create CloudFront distribution to serve our avatar uploads from S3 much faster. 
    1. Navigate to **CloudFront**
    2. Click on **Create Distribution**
    3. Origin Domain should be where our assets are stored (e.g `assets.<domain_name>`)
    4. Choose **Origin access control settings (recommended)**
    5. Viewer protocol policy should be `Redirect HTTP to HTTPS`
    6. Choose `Cache policy and origin request policy (recommended)`
    7. Cache Policy of `CachingOptimized`
    8. Tick `Use all edge locations`
    9. Set Alternate domain name (CNAME) as your `assets.<domain_name>`
    10. Use the SSL Certificate generated from our ACM
    11. Everything else leave as default
   
  - After creating the distribution, we need to create an Alias from hosted zone pointing to our cloudfront distribution
    1. Go to Route 53
    2. Record name add `assets`.<your_domain>
    3. Turn on `Alias`
    4. Route traffic to `Alias to CloudFront Distribution`
    5. Choose our created CloudFront distribution 
  
  
  - Added a bash script for `sharp` modules installation on the aws/lambdas/process images folder [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/c6a8d748784775cd879052ec5a13785cacfbd7bb#diff-960a36189353820d27f8f067245981b58a86987eb66e9cf2260266b521955fc1)
  

### 3. Implement Users Profile Page
 
##### Context:
  - Add functionalities to our Users Profile Page where the Avatar images will be rendered as well as other information about the user (e.g `name`,`handle`, `bio`)
  
  - Added a modification to the backend Dockerfile for debugging assistance [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/83589235c73bab71d925f6e07debe1ccefa4517b#diff-c176a487f689a4982c737a1774a9eb0ff6df3ee02ec6c6bc981d27f56e4799ad). This will allow us to see the print when debugging
  
  - Also added the ECR login in our gitpod startup [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/b789a1f06119e7d2e1c86b0bb7dddb5364ae1295). Saves a bit of time.
  
  - Also created a script to run all necessary database scripts for our development [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/240f6c19d27059d0202a40f85dfa0fa30ac3ed24)

  - This [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/ea2f21e86d676e3e4470cd0e9b05037c7e39ba05) helps makes pathing less complicated for our frontend (e.g ../component/ProfileForm.js ---> /component/ProfileForm.js

  - 
  
  - Modified the following components and pages in the frontend from [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/8d6d4cff6bb86e0454c614dcb80a4b8394c23456) and [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/c68d54dff1efeeb75a86bea01d668e1107433b48#diff-f5a1708fa9e56be428a37d6314e4ad7be8af74d9332ada2bc16913095fb0b4c6)
    - `ActivityFeed.js` ---> 
    - `CrudButton.js` ---> Added preventDefault()
    - `EditProfileButton.css` ---> Created
    - `EditProfileButton.js` ---> Created 
    - `ProfileHeading.css` ---> Created
    - `ProfileHeading.js` ---> Created
    - `HomeFeedPage.js` ---> Added ActivityFeed heading
    - `NotificationsFeedPage.js` ---> Added ActivityFeed heading
    - `UserFeedPage.js`  ---> Implemented access tokens and added profile components to render display_name and handler information
  
  - Created a `show.sql` to show the data from database in the ProfilePage section [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/8d6d4cff6bb86e0454c614dcb80a4b8394c23456#diff-07ce02305090a7c99db6c3979565f0f92196574901638f8f6b8f12659045da0f) 
 
  - Result should show the Users Profile Page rendering the data of the logged in user.
  
  ![image](https://user-images.githubusercontent.com/56792014/233612259-d34de5a2-810d-4639-b9f4-0bb368959c77.png)


### 4. Implement Users Profile Form

##### Context:

  - Added a Profile Form for uploading Avatar and rendering them to our ProfilePage
    - `ProfileForm.css` and `ProfileForm.js` are created [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/c34c0fc41bda7911e839617a169ff8f43c14cc21#diff-8b72e4ebe6afc9b82fcdb1f144c2859c958ab22b41da71a16b22e3477411589b) 
    - `UserFeedPage.js` is modified to connect ProfileForm pages into it.

    - Result should be able to show the ProfileForm with the update button in the Profile Page

### 5. Implement Backend Migrations
  
##### Context:
  - db Migration is needed as we have to update our postgres with a new column called `bio`. This `bio` data will be present to the Profile page and will be updated by the Profile Form
  
  - Create a `./backend-flask/db/migrations` folder, this will contain the files generated from the `./bin/generate/migration` script
  - In our bin folder, a `/generate/migration` script will be created. This will create a python script that can run a sql command of adding a column_bio and deleting it.
  - Also in our bin folder, a `/db/migrate` script and `/db/rollback` script will be created. The migrate script will add the bio column whilst the rollback will delete thie bio column.
  - The components are also modified during the implementation of backend migrations.
    - `Popup.css` ---> Created for ProfileForm popup effect
    - `ProfileForm.css` ---> Modified css design
    - `ProfileForm.js` ---> Modified to include users.bio
    - `ProfileHeading.css` ---> Modified css design
    - `ProfileHeading.js` ---> Modified to include users.bio
    - `ReplyForm.css` ---> Modified css design for popup effect
    - `ReplyForm.js` ---> Added on-click close

  - End result should be the local db table will show the bio column after running the  
 
 ```sh
 ./bin/generate/migration
 ./bin/db/migrate
 ```


### 6. Create JWT Lambda Layer and API Gateway

##### Context:
  - Create lambda layers for our Lambda JWT Authorizer
  
  - We will also modify our lambda function `Cruddur-Upload-Avatar` and `lambda-authorizer` to prevent cors issues and decode the JWT token. [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-6634d051c2513348146b502332d389c24b71f341c9dadc79920f038477847d8b) and [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-8bb1ceece57f661ba58a537e598e8341708a57e707267ea40b4b3470b1f8a0fb). This will be posted as code in their lambda functions names respectively in AWS Lambda
  
  - We will also add env vars for the CruddurApiGatewayLambdaAuthorizer which is `USER_POOL_ID` and `CLIENT_ID` 
  
  - We will also add a CORS for our s3 bucket for Uploaded Avatars [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-6ec389d0dc9ebe74ed6bedc9153a385fafc9f8375f0530d2e88369670034c57c)
  
  - In this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-15a93ce383061e0d60c29596313d0c887c7bfdc7e8b24cde175e3dce0bc7b917), we will create a ./lambda-layers/ruby-jwt. Uploading this as a lambda layer for our `CruddurApiGatewayLambdaAuthorizer`
  
  - We will create a API endpoint in API Gateway (e.g api.<domain_name>), this will added as a front-end env var [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-35a5ccc4d959134edbd6e6fcb0cbaef9d9b9587320e1404216cfddfd44332ed8). This will be referenced as the `gateway_url` in `ProfileForm.js` and `ProfileHeading.js` from [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-ade7dd0431c1f2f971f780b90fb5fd250827bf96b8a1a5b573c073ab6d460028) and [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/95b4efb0022813591797f4f2b56978ce9b0d1d4a#diff-64a5613aeb23a2f2ecdacb22fbb1e625f46ba13dfeab7a32fded8c4e51381bc5)
  
  - In API Gateway, Go to the created API which in my case is `api.thecloudstore.project`.
  - Create a route called `/avatars/key_upload`, attach the authorizer `CruddurJWTAuthorizer` with the lambda function as `CruddurApiGatewayLambdaAuthorizer`. The integration would be the lambda function `CruddurAvatarUpload`
  - Create another route again called `/{proxy+}` this will help prevent cors issue. This will not have any authorizer but instead an integration would be attached which is `CruddurAvatarUpload`

  - End result would be successfully uploading the image with our API endpoints without cors issue
  

### 7. Render Avatars in App via CloudFront

##### Context:
  
  - Modified the following components in this [commit](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/813afbc966d722a72bbcf7a73b128eb8a73658a0#diff-07ce02305090a7c99db6c3979565f0f92196574901638f8f6b8f12659045da0f) 
    - `ProfileAvatar.css` ---> Created
    - `ProfileAvatar.js` ---> Created 
    - `ProfileForm.css` ---> Modified to render the html properly
    - `ProfileHeading.css` ---> Modified to render the html properly
    - `ProfileHeading.js` ---> Integrated ProfileAvatar to html codes
    - `ProfileInfo.js` ---> Integrated ProfileAvatar to html codes
  - Also added the cognito_user_id as cognito_user_uuid to reference our user from AWS Cognito in the ProfileForm [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/813afbc966d722a72bbcf7a73b128eb8a73658a0#diff-07ce02305090a7c99db6c3979565f0f92196574901638f8f6b8f12659045da0f)
    - `CheckAuth.js` is modified to add other cognito_user.attributes.sub in the setUser [here](https://github.com/aynfrancesco06/aws-bootcamp-cruddur-2023/commit/813afbc966d722a72bbcf7a73b128eb8a73658a0#diff-716a46d7255bdc7f3c7c1f5f463d4580b0f4dcb288e9027b432ea13e8baebdf9)
   
   - End result should look like this

![image](https://user-images.githubusercontent.com/56792014/233633273-397f2a8d-7c70-47a6-8f28-5be797e6dee8.png)


Notes:
  - Got stuck with the CORS issue and a bootcamper's notes assisted me with troubleshooting the issue. I've also gone with the bootcampers' route of passing the JWT sub from `CruddurAPIGatewayLambdaAuthorizer` to `CruddurAvatarUpload` instead of having a layer of JWT. [ref](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html)
 
 
 
