import boto3
import sagemaker
from sagemaker import serializers, deserializers

def main():
    boto3.Session(profile_name='sagemaker-user', region_name='eu-north-1')
    sagemaker_session = sagemaker.Session(boto3.session.Session())

    endpoint_name = "gptj-ds-2023-05-16-20-26-21-253"

    predictor = sagemaker.Predictor(
        endpoint_name=endpoint_name,
        sagemaker_session=sagemaker_session,
        serializer=serializers.JSONSerializer(),
        deserializer=deserializers.JSONDeserializer(),
    )
    response = predictor.predict(
        data ={"inputs": "Large model inference is", "parameters": {"max_length": 50, "temperature": 0.5}}
    )
    print(response)

if __name__ == "__main__":
    main()