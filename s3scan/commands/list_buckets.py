# list_buckets.py
import click
import boto3

@click.command()
@click.pass_context
def list_buckets(ctx ):
    # make an instance of boto3 client
    s3 = boto3.client("s3", 
                    endpoint_url=ctx.obj["endpoint_url"],
                    region_name=ctx.obj["region"],
                    aws_access_key_id=ctx.obj["access_key_id"],
                    aws_secret_access_key=ctx.obj["secret_access_key"]
    )
    
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        click.echo(bucket["Name"])
  