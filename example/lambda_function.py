from names_generator import generate_name  # noqa


def lambda_handler(event, context):  # noqa
    """
    This is the main function that is executed by AWS Lambda.

    :param event:
    :param context:
    :return:
    """
    return {
        "statusCode": 200,
        "body": f"Hello from Lambda!. I see you are using {generate_name()} as your name.",
    }
