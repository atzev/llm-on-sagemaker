import sagemaker
from sagemaker.model import Model
from sagemaker import serializers, deserializers
from sagemaker import image_uris
import boto3
import jinja2
from pathlib import Path


def deploy_model(image_uri, model_data, role, endpoint_name, instance_type, sagemaker_session):
    """Helper function to create the SageMaker Endpoint resources and return a predictor"""
    model = Model(image_uri=image_uri, model_data=model_data, role=role)

    model.deploy(initial_instance_count=1, instance_type=instance_type, endpoint_name=endpoint_name)

    # our requests and responses will be in json format so we specify the serializer and the deserializer
    predictor = sagemaker.Predictor(
        endpoint_name=endpoint_name,
        sagemaker_session=sagemaker_session,
        serializer=serializers.JSONSerializer(),
        deserializer=deserializers.JSONDeserializer(),
    )

    return predictor

def main():
    role="arn:aws:iam::XXXXXXX:role/service-role/AmazonSageMaker-ExecutionRole-XXXXXX" #REPLACE WITH YOUR ROLE
    boto3.Session(profile_name='sagemaker-user', region_name='eu-north-1')
    sess = sagemaker.Session(boto3.session.Session())

    bucket = sess.default_bucket()  # bucket to house artifacts
    s3_code_prefix = "large-model-djl-gptj6b/code"  # folder within bucket where code artifact will go
    region = sess._region_name  # region name of the current SageMaker Studio environment
    jinja_env = jinja2.Environment()  # jinja environment to generate model configuration templates
    

    pretrained_model_location = f"s3://sagemaker-examples-files-prod-{region}/models/gpt-j-6b-model/" #REPLACE WITH YOUR OWN LOCATION
    print(f"Pretrained model will be downloaded from ---- > {pretrained_model_location}")

    # creates a unique endpoint name
    hf_endpoint_name = sagemaker.utils.name_from_base("gptj-acc")
    print(f"Our endpoint will be called {hf_endpoint_name}")

    template = jinja_env.from_string(Path("deepspeed_src/serving.template").open().read())
    Path("deepspeed_src/serving.properties").open("w").write(
        template.render(s3url=pretrained_model_location)
    )

    #AWS CLI: tar czvf ds_model.tar.gz deepspeed_src/
    ds_s3_code_artifact = sess.upload_data("ds_model.tar.gz", bucket, s3_code_prefix)


    inference_image_uri = (
        f"763104351884.dkr.ecr.{region}.amazonaws.com/djl-inference:0.20.0-deepspeed0.7.5-cu116" ##REPLACE WITH THE IMAGE FOR THE FRAMEWORK VERSIONS YOU ARE USING from  https://docs.aws.amazon.com/sagemaker/latest/dg/large-model-inference-dlc.html
    )  

    
    print(f"S3 Code or Model tar ball uploaded to --- > {ds_s3_code_artifact}") 

    ds_endpoint_name = sagemaker.utils.name_from_base("gptj-ds")
    ds_predictor = deploy_model(
        image_uri=inference_image_uri,
        model_data=ds_s3_code_artifact,
        role=role,
        endpoint_name=ds_endpoint_name,
        instance_type="ml.g4dn.4xlarge",
        sagemaker_session=sess
    )

if __name__ == "__main__":
    main()