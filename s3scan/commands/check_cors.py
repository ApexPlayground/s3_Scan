#check_cors.py
import click
import boto3
import json

@click.command()
@click.option("--bucket", required=True, help="Name of the S3 bucket to audit for CORS misconfigurations")
@click.pass_context
def check_cors(ctx, bucket):
    error_count = 0
    s3 = boto3.client("s3", 
                    endpoint_url=ctx.obj["endpoint_url"],
                    region_name=ctx.obj["region"],
                    aws_access_key_id=ctx.obj["access_key_id"],
                    aws_secret_access_key=ctx.obj["secret_access_key"]
    )
    try:
        response = s3.get_bucket_cors(Bucket=bucket)
        rules = response["CORSRules"]
        click.echo(f"CORS rules set to your bucket\n{json.dumps(rules, indent=2)}")
        
        misconfigured = False
        

        for rule in rules:
            danger_methods = ["PUT", "DELETE", "POST"]
            allows_all_origins = "*" in rule["AllowedOrigins"]
            allows_dangerous_methods = any(method in rule["AllowedMethods"] for method in danger_methods)
            
            if allows_all_origins and allows_dangerous_methods:
                misconfigured = True
                click.secho("WARNING: Bucket allows dangerous methods from any origin!", fg="red", bold="True")
                click.secho(
                    "Suggestion: Restrict AllowedOrigins to your app or remove PUT/POST/DELETE "
                    "if the bucket is meant to be public-read only.", fg="yellow"
                )
                error_count += 1
                click.echo(" ")
            
            # all headers allowed
            if "*" in rule.get("AllowedHeaders", []):
                misconfigured = True
                click.secho("WARNING: All headers allowed!", fg="red", bold=True)
                click.secho("Suggestion: Restrict AllowedHeaders to only what your app needs.", fg="yellow")
                error_count += 1
                click.echo(" ")
                
            if "*" in rule.get("ExposeHeaders", []):
                misconfigured = True
                click.secho("WARNING: All headers exposed to client!", fg="red", bold=True)
                error_count += 1
                click.echo(" ")
            
            # long max age
            max_age = rule.get("MaxAgeSeconds", 0)
            if max_age > 3600:  # example threshold
                click.secho(f"NOTICE: MaxAgeSeconds is very high ({max_age})", fg="yellow")
                error_count += 1
                click.echo(" ")


            
          
        
        if not misconfigured:
            click.echo(f"Your CORS config for {bucket} looks good")
            
    
    except Exception as ex:
        click.secho(f"Unexpected error:{ex}", fg="red", bold="True")

    return error_count
    
        
