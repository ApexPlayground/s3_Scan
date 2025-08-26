#check_cors.py
import click
import boto3

@click.command()
@click.option("--bucket", required=True, help="AWS s3 bucket to check")
@click.pass_context
def check_cors(ctx, bucket):
    s3 = boto3.client("s3", 
                    endpoint_url=ctx.obj["endpoint_url"],
                    region_name=ctx.obj["region"],
                    aws_access_key_id=ctx.obj["access_key_id"],
                    aws_secret_access_key=ctx.obj["secret_access_key"]
    )
    try:
        response = s3.get_bucket_cors(Bucket=bucket)
        rules = response["CORSRules"]
        click.echo(f"Rules set to your bucket\n{rules}")
        
        misconfigured = False

        for rule in rules:
            danger_methods = ["PUT", "DELETE", "POST"]
            allows_all_origins = "*" in rule["AllowedOrigins"]
            allows_dangerous_methods = any(method in rule["AllowedMethods"] for method in danger_methods)
            
            if allows_all_origins and allows_dangerous_methods:
                misconfigured = True
                click.echo("WARNING: Bucket allows dangerous methods from any origin!")
                click.echo(
                    "Suggestion: Restrict AllowedOrigins to your app or remove PUT/POST/DELETE "
                    "if the bucket is meant to be public-read only."
                )
            
            # change flag to false
          
        
        if not misconfigured:
            click.echo(f"Your CORS config for {bucket} looks good")
            
    
    except Exception as ex:
         click.echo(f"Unexpected error:{ex}")
    
        
