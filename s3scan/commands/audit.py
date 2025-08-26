# commands/audit.py
import click
from . import check_acl, check_cors, check_versioning, check_policy

@click.command()
@click.option("--bucket", required=True, help="AWS S3 bucket to audit")
@click.pass_context
def audit(ctx, bucket):
    """Run a full security audit on a bucket"""
    click.secho(f"Starting full audit for bucket: {bucket}", fg="cyan", bold=True)

    # invoke each command safely
    ctx.invoke(check_acl.check_acl, bucket=bucket)
    ctx.invoke(check_cors.check_cors, bucket=bucket)
    ctx.invoke(check_versioning.check_versioning, bucket=bucket)
    ctx.invoke(check_policy.check_policy, bucket=bucket)

    click.secho(f"Audit completed for bucket: {bucket}", fg="cyan", bold=True)
