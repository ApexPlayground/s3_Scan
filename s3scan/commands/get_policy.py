#check_policy.py
import click
import boto3
import json

@click.command()
@click.option("--bucket", required=True, help="Provide valid bucket to check policy")
@click.pass_context
def check_policy(ctx, bucket):
    s3 = boto3.client("s3", 
                    endpoint_url=ctx.obj["endpoint_url"],
                    region_name=ctx.obj["region"],
                    aws_access_key_id=ctx.obj["access_key_id"],
                    aws_secret_access_key=ctx.obj["secret_access_key"]
    )
    try:
        response = s3.get_bucket_policy(Bucket=bucket)
        policy = json.loads(response["Policy"])
        click.echo(f"Policy set on bucket with name {bucket}:\n {json.dumps(policy, indent=2)}")
        
        misconfigured = False
        
        for val in policy.get("Statement", []):
            effect = val.get("Effect", "")
            principal = val.get("Principal", {})
            action = val.get("Action", [])
            resource = val.get("Resource", [])
        
            #normalize: convert to list incase of single string
            if isinstance(action, str):
                action = [action]
            if isinstance(resource, str):
                resource = [resource]
            
            #check if public and has dangerous actions allowed
            if principal == "*" or (isinstance(principal, dict) and principal.get("AWS") == "*"):
                danger_actions = ["s3:PutObject", "s3:DeleteObject", "s3:PostObject"]
                if any(item in action for item in danger_actions):
                    misconfigured = True
                    click.secho("WARNING: Public access with dangerous actions detected!", fg="red", bold="True")
                    click.secho("Suggestion: Remove '*' principal or restrict actions to least privilege.", fg="yellow")
                
            
        if not misconfigured:
            click.secho("policy configuration looks good", fg="green")
        
    except Exception as ex:
        click.echo(f"Unexpected error: {ex}")
        
    
    