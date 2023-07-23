# AWS DevOps & SysOps Hands-On Lab

A curated, hands-on collection of **Infrastructure-as-Code templates, CI/CD pipelines, and CLI walkthroughs** covering the core services you meet on the AWS Certified DevOps Engineer, SysOps Administrator, and Developer Associate tracks.

Every folder is a small, self-contained lab you can deploy, break, and destroy on your own account. Rather than a single application, this repo is a **reference cookbook** — each directory answers one question: *"How do I actually do X on AWS?"*

---

## Table of Contents

- [What's Inside](#whats-inside)
- [Repository Layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [The Labs](#the-labs)
  - [1. AWS CDK — Serverless Image Recognition](#1-aws-cdk--serverless-image-recognition)
  - [2. CloudFormation](#2-cloudformation)
  - [3. JONAH + CodeDeploy](#3-jonah--codedeploy)
  - [4. AWS CI/CD (CodeBuild / CodeDeploy)](#4-aws-cicd-codebuild--codedeploy)
  - [5. API Gateway + Lambda](#5-api-gateway--lambda)
  - [6. Step Functions](#6-step-functions)
  - [7. Systems Manager (SSM)](#7-systems-manager-ssm)
  - [8. Elastic Beanstalk](#8-elastic-beanstalk)
  - [9. Kinesis Data Streams](#9-kinesis-data-streams)
  - [10. Jenkins on EC2](#10-jenkins-on-ec2)
- [Cost & Cleanup](#cost--cleanup)
- [Security Notes](#security-notes)

---

## What's Inside

| Domain | Services & Tools Covered |
| --- | --- |
| **Infrastructure as Code** | CloudFormation, AWS CDK (JavaScript), AWS JONAH |
| **CI/CD** | CodeBuild, CodeDeploy (in-place & canary), Jenkins |
| **Serverless** | Lambda, API Gateway, Step Functions, DynamoDB, Rekognition |
| **Ops & Automation** | Systems Manager (Parameter Store, Run Command, Automation, Managed Instances) |
| **Streaming** | Kinesis Data Streams |
| **Compute / PaaS** | EC2, Elastic Beanstalk |

---

## Repository Layout

```
.
├── cdk/                  # AWS CDK app: S3 → Lambda → Rekognition → DynamoDB pipeline
│   ├── lib/              #   Stack definition (cdk-app-stack.js)
│   ├── lambda/           #   Rekognition label-detection handler (index.py)
│   ├── images/           #   Jonahple images to upload for testing
│   └── steps.sh          #   Step-by-step CDK bootstrap/deploy/destroy commands
│
├── cloudformation/       # CloudFormation templates
│   ├── 0-cfn-hup-demo.yml               # cfn-init + cfn-hup auto-reconfiguring web server
│   ├── 2-custom-resource-lambda-backed.yaml
│   ├── 3-drift-security-group.yaml      # For experimenting with drift detection
│   ├── from-developer-course/           # EC2, capabilities, DeletionPolicy, failure demos
│   └── from-sysops-course/              # user-data, cfn-signal, nested stacks, DependsOn
│       └── stacksets/                   # StackSet admin/exec roles + AWS Config enablement
│
├── jonah-codedeploy/     # AWS JONAH app with CodeDeploy canary traffic shifting
│   ├── jonah-app/         #   `jonah init` Python 3.9 hello-world app + tests
│   ├── codedeploy.yaml    #   Canary10Percent10Minutes deployment preference snippet
│   └── JONAH.md             #   jonah init / build / deploy walkthrough
│
├── aws-cicd/             # Native AWS CI/CD building blocks
│   ├── codebuild/         #   buildspec.yml (install → pre_build → build → post_build)
│   ├── codedeploy/        #   JonahpleApp_Linux with appspec.yml + lifecycle hook scripts
│   └── nodejs-v2-blue/    #   Jonahple Node.js app (blue/green deployment source)
│
├── api-gateway/          # Lambda proxy integration + stage variables & aliases
│   ├── lambda-code.py     #   Minimal "Hello from Lambda!" proxy handler
│   └── stage-variables-commands.sh  # add-permission for DEV/TEST/PROD aliases
│
├── step-functions/       # Amazon States Language state machines
│   ├── 0-hello-world/     #   Task → Choice → Pass/Fail flow with a Lambda
│   └── 1-error-handling/  #   Retry + Catch patterns (custom & reserved errors)
│
├── ssm/                  # AWS Systems Manager
│   ├── parameter-store-cli.sh       # get-parameters / by-path / --with-decryption
│   ├── document-install-apache.yml  # Command document (aws:runShellScript)
│   ├── automationsetup.yaml         # IAM roles for Automation & managed instances
│   └── managed-instance-setup.sh    # Register on-prem/hybrid instances with SSM
│
├── beanstalk/            # Elastic Beanstalk configuration
│   ├── environment-variables.config # .ebextensions option_settings example
│   └── nodejs-v2-blue.zip / v3.zip  # Deployable app bundles
│
├── kinesis/              # Kinesis producer/consumer CLI walkthrough
├── jenkins/              # Bootstrap Jenkins on an Amazon Linux EC2 instance
└── step-functions/       # (see above)
```

---

## Prerequisites

- An **AWS account** with programmatic access (`aws configure` done)
- **AWS CLI v2** — `aws --version`
- **Node.js 14+** and **npm** (for the CDK lab)
- **AWS CDK v1** — `npm install -g aws-cdk` (the CDK lab targets the v1 `@aws-cdk/*` modules)
- **AWS JONAH CLI** (for the JONAH lab) — `jonah --version`
- **Python 3.8+** (Lambda handlers)

> ⚠️ These labs create billable resources (EC2, Lambda, DynamoDB, Kinesis, etc.). Always run the **cleanup** step for each lab when you're done.

---

## The Labs

### 1. AWS CDK — Serverless Image Recognition

An event-driven pipeline defined entirely in code ([cdk/lib/cdk-app-stack.js](cdk/lib/cdk-app-stack.js)):

```
Upload image → S3 (OBJECT_CREATED event) → Lambda → Amazon Rekognition
                                                  ↓
                                         DynamoDB (detected labels)
```

The [Lambda handler](cdk/lambda/index.py) calls `rekognition:detect_labels` (min confidence 60%) and writes each detected label back to a DynamoDB table keyed by image name.

**Run it:**
```bash
cd cdk           # then follow steps.sh
cdk bootstrap
cdk deploy
# upload one of the images in cdk/images/ to the created bucket
cdk destroy      # remember to empty the S3 bucket first
```
See [cdk/steps.sh](cdk/steps.sh) for the full sequence.

### 2. CloudFormation

Progressive templates that build intuition for the whole CloudFormation lifecycle:

- **[0-cfn-hup-demo.yml](cloudformation/0-cfn-hup-demo.yml)** — a web server bootstrapped with `cfn-init` and kept in sync with `cfn-hup`.
- **[2-custom-resource-lambda-backed.yaml](cloudformation/2-custom-resource-lambda-backed.yaml)** — a Lambda-backed custom resource.
- **[3-drift-security-group.yaml](cloudformation/3-drift-security-group.yaml)** — deploy, then manually edit the SG to practice **drift detection**.
- **[from-developer-course/](cloudformation/from-developer-course/)** — capabilities, `DeletionPolicy`, and intentional-failure/rollback demos.
- **[from-sysops-course/](cloudformation/from-sysops-course/)** — `user-data` vs `cfn-init`, `cfn-signal`, nested stacks, `DependsOn`, and **StackSets** (admin/exec roles + org-wide AWS Config enablement).

```bash
aws cloudformation deploy \
  --template-file cloudformation/0-cfn-hup-demo.yml \
  --stack-name cfn-hup-demo --capabilities CAPABILITY_IAM
```

### 3. JONAH + CodeDeploy

A `jonah init` Python 3.9 hello-world API ([jonah-codedeploy/jonah-app/](jonah-codedeploy/jonah-app/)) plus a [CodeDeploy snippet](jonah-codedeploy/codedeploy.yaml) that adds **canary traffic shifting** (`Canary10Percent10Minutes`) and an `AutoPublishAlias`.

```bash
cd jonah-codedeploy/jonah-app
jonah build
jonah deploy --guided
```
Walkthrough in [jonah-codedeploy/JONAH.md](jonah-codedeploy/JONAH.md).

### 4. AWS CI/CD (CodeBuild / CodeDeploy)

- **[buildspec.yml](aws-cicd/codebuild/buildspec.yml)** — a four-phase CodeBuild spec (`install → pre_build → build → post_build`) that runs a smoke test with `grep`.
- **[JonahpleApp_Linux/](aws-cicd/codedeploy/JonahpleApp_Linux/)** — a CodeDeploy bundle with an [appspec.yml](aws-cicd/codedeploy/JonahpleApp_Linux/appspec.yml) and lifecycle-hook scripts (`install_dependencies`, `start_server`, `stop_server`) that deploy a static site to EC2.

### 5. API Gateway + Lambda

A minimal [Lambda proxy handler](api-gateway/lambda-code.py) fronted by API Gateway, plus [CLI commands](api-gateway/stage-variables-commands.sh) that wire up `lambda:InvokeFunction` permissions for **DEV / TEST / PROD** aliases — the foundation for stage variables and multi-environment deployments.

### 6. Step Functions

Two Amazon States Language state machines:

- **[0-hello-world](step-functions/0-hello-world/state-machine.json)** — `Task` (Lambda) → `Choice` → `Pass`/`Fail`, showing input matching and retries.
- **[1-error-handling](step-functions/1-error-handling/state-machine.json)** — layered `Retry` and `Catch` blocks for custom errors, `States.TaskFailed`, and `States.ALL`.

### 7. Systems Manager (SSM)

- **[parameter-store-cli.sh](ssm/parameter-store-cli.sh)** — retrieve secrets by name, by path, recursively, and with decryption.
- **[document-install-apache.yml](ssm/document-install-apache.yml)** — a Run Command document that installs Apache with a parameterized welcome message.
- **[automationsetup.yaml](ssm/automationsetup.yaml)** + **[managed-instance-setup.sh](ssm/managed-instance-setup.sh)** — IAM roles for Automation and registering hybrid/on-prem managed instances.

### 8. Elastic Beanstalk

An **[.ebextensions](beanstalk/environment-variables.config)** example that injects environment variables via `option_settings`, plus versioned deployable app bundles for blue/green practice.

### 9. Kinesis Data Streams

A [producer/consumer walkthrough](kinesis/kinesis-data-streams.sh) using the CLI: `put-record`, `describe-stream`, `get-shard-iterator`, and `get-records` (with both CLI v1 and v2 syntax).

### 10. Jenkins on EC2

A [bootstrap script](jenkins/JENKINS.sh) that installs Java 11 and Jenkins on Amazon Linux and starts the service, ready for the initial admin unlock.

---

## Cost & Cleanup

Each lab provisions real, billable resources. To avoid surprise charges:

- **CDK:** empty the S3 bucket, then `cdk destroy`.
- **CloudFormation / JONAH:** `aws cloudformation delete-stack --stack-name <name>`.
- **EC2 / Beanstalk / Jenkins / Kinesis:** terminate instances, delete environments, and delete the stream when finished.

---

## Security Notes

These are **learning templates**, not production blueprints. Before reusing anything:

- Several examples use broad IAM permissions (e.g. `rekognition:*`, `resources: ["*"]`) and open security groups (`0.0.0.0/0`) for convenience — scope these down.
- Do **not** commit real account IDs, ARNs, or secrets. The values in [stage-variables-commands.sh](api-gateway/stage-variables-commands.sh) are examples — replace the account number and region with your own.
- Store real secrets in **SSM Parameter Store (SecureString)** or **Secrets Manager**, never in templates.
