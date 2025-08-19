#check_acl.py
import click
import boto3

@click.command()
@click.option("--bucket", required=True, help="AWS s3 bucket to check")
@click.pass_context
def check_acl(ctx, bucket):
     s3 = boto3.client("s3", 
                    endpoint_url=ctx.obj["endpoint_url"],
                    region_name=ctx.obj["region"],
                    aws_access_key_id=ctx.obj["access_key_id"],
                    aws_secret_access_key=ctx.obj["secret_access_key"]
    )
     response = s3.get_bucket_acl(Bucket=bucket)

     for grant in response["Grants"]:
          grantee = grant["Grantee"]
          permission = grant["Permission"]

          #conditions to check permissions
          if grantee.get("Type") == "Group" and "AllUser" in grantee.get("URI", ""):
               click.echo(f"Bucket with name: {bucket} is PUBLIC with permission:{permission}")
          else:
            click.echo(f"Bucket {bucket} grant: {grantee} → {permission}")
        
           

