#!/bin/bash

FUNCTION_NAME=tweet-bookmeter-summary
MODULE_NAME=tweet_bookmeter_summary

rm -f lambda.zip

poetry export -f requirements.txt --output src/$MODULE_NAME/requirements.txt

pushd src/$MODULE_NAME
    poetry run pip install -r requirements.txt -t .
    zip -rq ../../lambda.zip .
popd

aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://lambda.zip
