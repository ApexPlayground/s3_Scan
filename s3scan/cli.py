# cli.py
import click
from commands import check_acl, check_cors, check_policy, check_versioning
from commands import list_all_buckets
from commands import audit

@click.group()
@click.option("--endpoint-url", default="http://localhost:4566", required=True, help="LocalStack endpoint")
@click.option("--region", default="us-east-1", required=True, help="AWS region")
@click.option("--access-key-id", default="test", required=True, help="AWS access key ID")
@click.option("--secret-access-key", default="test", required=True, help="AWS secret access key")
@click.pass_context
def cli(ctx, endpoint_url, region, access_key_id, secret_access_key):
    # store in context object
    ctx.obj = {
        "endpoint_url": endpoint_url,
        "region": region,
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key
    }

# add commands
cli.add_command(list_all_buckets.list_buckets)
cli.add_command(check_acl.check_acl)  
cli.add_command(check_cors.check_cors)
cli.add_command(check_policy.check_policy)
cli.add_command(check_versioning.check_versioning)
cli.add_command(audit.audit)

if __name__ == "__main__":
    cli()