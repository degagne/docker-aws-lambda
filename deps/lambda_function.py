# This file is a boilerplate for AWS Lambda functions.

# When a new image is build, this file should be overridden with the actual
# implementation of the Lambda function.


def lambda_handler(event, context):  # noqa
    """
    This is the main function that is executed by AWS Lambda.

    :param event:
    :param context:
    :return:
    """
    return {
        "statusCode": 406,
        "body": """
            ***********
            HELLO!
            
            IF YOU SEE THIS MESSAGE, IT INDICATES THAT YOUR AMAZON LAMBDA IMAGE
            IS WORKING PROPERLY, BUT IT HAS NOT BEEN CONFIGURED YET.
            
            YOU MUST OVERRIDE THIS FUNCTION WITH YOUR OWN IMPLEMENTATION.
            ***********
        """
    }
