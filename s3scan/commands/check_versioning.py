# check_versioning.py
import click
import boto3

@click.command()
@click.option("--bucket", required=True, help="Name of the S3 bucket to check versioning")
@click.pass_context
def check_versioning(ctx, bucket):
    """Check versioning"""
    error_count = 0
    s3 = boto3.client(
        "s3",
        endpoint_url=ctx.obj["endpoint_url"],
        region_name=ctx.obj["region"],
        aws_access_key_id=ctx.obj["access_key_id"],
        aws_secret_access_key=ctx.obj["secret_access_key"]
    )

    try:
        response = s3.get_bucket_versioning(Bucket=bucket)
        status = response.get("Status", "Disabled")
       

        if status == "Enabled":
            click.secho(f"Bucket '{bucket}' has versioning ENABLED.", fg="green", bold=True)
            click.echo(" ")
            
        elif status == "Suspended":
            click.secho(f"Bucket '{bucket}' has versioning SUSPENDED.", fg="yellow", bold=True)
            click.secho("Suggestion: Enable versioning to protect against accidental deletion/overwrite.", fg="yellow")
            click.echo(" ")
            error_count += 1
        else:
            click.secho(f"WARNING: Versioning NOT ENABLED for bucket '{bucket}'!", fg="red", bold=True)
            click.secho("Suggestion: Enable versioning using:\n"
                        f"aws s3api put-bucket-versioning --bucket {bucket} --versioning-configuration Status=Enabled", fg="yellow")
            click.echo(" ")
            error_count += 1

    except Exception as ex:
        click.secho(f"Unexpected error: {ex}", fg="red", bold=True)
        error_count += 1
        click.echo(" ")
    
    return error_count
