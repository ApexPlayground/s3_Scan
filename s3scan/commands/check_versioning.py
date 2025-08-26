# check_versioning.py
import click
import boto3

@click.command()
@click.option("--bucket", required=True, help="AWS S3 bucket to check")
@click.pass_context
def check_versioning(ctx, bucket):
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
        else:
            click.secho(f"WARNING: Versioning NOT ENABLED for bucket '{bucket}'!", fg="red", bold=True)
            click.secho("Suggestion: Enable versioning using:\n"
                        f"aws s3api put-bucket-versioning --bucket {bucket} --versioning-configuration Status=Enabled", fg="yellow")
            click.echo(" ")

    except Exception as ex:
        click.secho(f"Unexpected error: {ex}", fg="red", bold=True)
