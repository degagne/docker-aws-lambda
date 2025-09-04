# Example

This example demonstrates how to use the docker images provided in this repository.

## Build the Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```powershell
docker build --build-arg LAMBDA_TASK_ROOT=/var/task --build-arg LAMBDA_USER=lambda-user --build-arg LAMBDA_GROUP=lambda-group -t aws-lamdba-example .
```

## Run the Docker Container

To run the Docker container, use the following command:

```powershell
docker run -p 9000:8080 aws-lamdba-example
```

This will start an interactive terminal session inside the container.

## Test the Lambda Function

You can test the Lambda function by sending a POST request to the local endpoint. Use the following `curl` command:

```powershell
Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -ContentType "application/json" -Body '{}'
```

This command sends an empty JSON object as the event to the Lambda function. You should see a response from the 
function indicating that it was invoked successfully.

For example, the response might look like this:

```text
StatusCode        : 200
StatusDescription : OK
                    Content-Length: 102
                    Content-Type: text/plain; charset=utf-8
                    Date: Thu, 04 Sep 2025 03:26:14 GMT

                    {"statusCode": 200, "body": "Hello from Lambda!. I see you are using priceless_mur...
Forms             : {}
Headers           : {[Content-Length, 102], [Content-Type, text/plain; charset=utf-8], [Date, Thu, 04 Sep 2025 03:26:14 GMT]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 102
```

## Stop the Docker Container

To stop the Docker container, you can use the following command:

```powershell
docker stop <container_id>
```

Replace `<container_id>` with the actual ID of the running container, which you can find by running `docker ps`.

## Clean Up

To remove the Docker image, use the following command:

```powershell
docker rmi aws-lamdba-example
```

This will delete the image from your local Docker repository.
