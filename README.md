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
