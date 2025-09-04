FROM ddegagne/aws-lambda:3.13-alpine3.22 AS final-image

# Set build arguments for Lambda user, group, and task root
ARG LAMBDA_USER
ARG LAMBDA_GROUP
ARG LAMBDA_TASK_ROOT

# Change to a non-root user for security
USER ${LAMBDA_USER}

# Create the Lambda task root directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the function code and requirements file for Python dependencies
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip config set global.trusted-host pypi.org \
    && pip install --target ${LAMBDA_TASK_ROOT} --requirement requirements.txt --upgrade

# Set the entrypoint for the Lambda function
ENTRYPOINT ["/var/task/lambda-entrypoint.sh"]

# Set the command to run the Lambda function handler
CMD ["lambda_function.lambda_handler"]
