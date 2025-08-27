# commands/audit.py
import click
from . import check_acl, check_cors, check_versioning, check_policy

@click.command()
@click.option("--bucket", required=True, help="AWS S3 bucket to audit")
@click.pass_context
def audit(ctx, bucket):
    """Run a full security audit on a bucket"""
    click.secho(f"Starting full audit for bucket: {bucket}", fg="cyan", bold=True)

    total_errors = 0

    # invoke each command and collect errors
    acl_errors = ctx.invoke(check_acl.check_acl, bucket=bucket)
    cors_errors = ctx.invoke(check_cors.check_cors, bucket=bucket)
    versioning_errors = ctx.invoke(check_versioning.check_versioning, bucket=bucket)
    policy_errors = ctx.invoke(check_policy.check_policy, bucket=bucket)

    total_errors = acl_errors + cors_errors + versioning_errors + policy_errors

    click.secho("\n=== Audit Summary ===", fg="blue", bold=True)
    click.secho(f"ACL issues: {acl_errors}", fg="red" if acl_errors else "green")
    click.secho(f"CORS issues: {cors_errors}", fg="red" if cors_errors else "green")
    click.secho(f"Versioning issues: {versioning_errors}", fg="red" if versioning_errors else "green")
    click.secho(f"Policy issues: {policy_errors}", fg="red" if policy_errors else "green")
    click.secho(f"Total issues found: {total_errors}", fg="red" if total_errors else "green", bold=True)

    click.secho(f"Audit completed for bucket: {bucket}", fg="cyan", bold=True)
