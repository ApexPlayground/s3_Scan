---
id: s3Scan
title: AWS S3 Security CLI
---

# S3scan

A CLI tool to **scan AWS S3 buckets for security misconfigurations**. Built with **Python, Click, and Boto3**, this tool helps developers and cloud engineers **audit bucket ACLs, CORS settings, policies, and versioning** quickly and safely.

---

## Features

- **ACL Checks:** Detect public buckets, broad write permissions, or FULL_CONTROL granted to non-owners.
- **CORS Checks:** Identify dangerous configurations like PUT/POST/DELETE allowed from all origins.
- **Versioning Check:** Warn if versioning is not enabled.
- **Policy Checks:** Parse bucket policies to find overly permissive or unsafe rules.
- **Full Audit Command:** Run all checks in one go and get a **summary report**.

---

## Technology

- **Python 3.12**: main language
- **Click**: for building the CLI
- **Boto3**: AWS SDK for Python
- **LocalStack**: optional local testing environment

---

## Usage

The CLI works with both **real AWS** and **LocalStack** (local testing).

- **AWS:** If you omit `--endpoint-url`, the CLI will use your configured AWS credentials from `~/.aws/credentials` or environment variables.
- **LocalStack:** The default `--endpoint-url` points to `http://localhost:4566`. You can override it if needed. Default credentials (`test` / `test`) are automatically used for LocalStack.

> Notes:
>
> - You only need to provide credentials once per terminal session if using AWS.
> - LocalStack works out of the box with default endpoint and test credentials.

---

## Usage Examples

This tool supports **both AWS and LocalStack**.

- For **AWS**, provide the region (`--region`), credentials are loaded from your environment or `~/.aws/credentials`.
- For **LocalStack**, make sure LocalStack is running and include the `--endpoint-url http://localhost:4566` flag.

---

### 1. List All Buckets

```bash
# LocalStack
s3scan --endpoint-url http://localhost:4566 --region us-east-1 list-buckets

# AWS
s3scan --region us-east-1 list-buckets
```

### 2. check-acl

```bash
# LocalStack
s3scan check-acl --bucket bucket-name

# AWS
s3scan --region us-east-1 check-acl --bucket bucket-name

```

### 3. check-cors

```bash
# LocalStack
s3scan check-cors --bucket bucket-name

# AWS
s3scan --region us-east-1 check-cors --bucket bucket-name
```

### 4. Check Bucket Policy

```bash
# LocalStack
s3scan check-policy --bucket bucket-name

# AWS
s3scan --region us-east-1 check-policy --bucket bucket-name
```

### 5. Check Versioning

```bash
# LocalStack
s3scan check-versioning --bucket bucket-name

# AWS
s3scan --region us-east-1 check-versioning --bucket bucket-name

```

### 6. Check Audit

```bash
# LocalStack
s3scan audit --bucket bucket-name

# AWS
s3scan --region us-east-1 audit --bucket bucket-name
```
