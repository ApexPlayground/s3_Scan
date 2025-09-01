# check_acl.py
import click
import boto3

@click.command()
@click.option("--bucket", required=True, help="Name of the S3 bucket to audit for ACL misconfigurations")
@click.pass_context
def check_acl(ctx, bucket):
     """Check for ACL misconfiguration"""
     error_count = 0
     s3 = boto3.client(
          "s3",
          endpoint_url=ctx.obj["endpoint_url"],
          region_name=ctx.obj["region"],
          aws_access_key_id=ctx.obj["access_key_id"],
          aws_secret_access_key=ctx.obj["secret_access_key"]
     )

     try:
          response = s3.get_bucket_acl(Bucket=bucket)
          is_misconfigured = False
          owner_id = response.get("Owner", {}).get("ID")

          for grant in response["Grants"]:
               grantee = grant["Grantee"]
               permission = grant["Permission"]

               # PUBLIC access
               if grantee.get("Type") == "Group":
                    uri = grantee.get("URI", "")
                    if "AllUsers" in uri:
                         click.secho(f"Bucket {bucket} is PUBLIC with permission: {permission}", fg="red", bold=True)
                         click.secho("Suggestion: Set ACL to private using: aws s3api put-bucket-acl --bucket {bucket} --acl private", fg="yellow")
                         is_misconfigured = True
                         click.echo(" ")
                         error_count += 1

                    elif "AuthenticatedUsers" in uri:
                         click.secho(f"Bucket {bucket} allows access to all authenticated AWS users! Permission: {permission}", fg="red", bold=True)
                         click.secho("Suggestion: Restrict ACL to specific IAM users or roles.", fg="yellow")
                         is_misconfigured = True
                         click.echo(" ")
                         error_count += 1

                    # broad write permissions
                    if permission in ["WRITE", "FULL_CONTROL"]:
                         click.secho(f"Bucket {bucket} grants {permission} to a group!", fg="red", bold=True)
                         click.secho("Suggestion: Limit write/delete permissions to specific IAM users or roles.", fg="yellow")
                         is_misconfigured = True
                         click.echo(" ")
                         error_count += 1

               # check owner mismatch for FULL_CONTROL
               elif grantee.get("Type") == "CanonicalUser":
                    if permission == "FULL_CONTROL" and grantee.get("ID") != owner_id:
                         click.secho(f"Bucket {bucket} has FULL_CONTROL granted to non-owner!", fg="red", bold=True)
                         click.secho("Suggestion: Only owner should have FULL_CONTROL.", fg="yellow")
                         is_misconfigured = True
                         error_count += 1
                         click.echo(" ")

          if not is_misconfigured:
               click.secho(f"Bucket {bucket} appears to be PRIVATE and secure.", fg="green")
               click.echo(" ")

     except Exception as ex:
          click.secho(f"Unexpected error: {ex}", fg="red", bold=True)
          error_count += 1
          click.echo(" ")
     
     return error_count