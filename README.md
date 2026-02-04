# 🔒 AWS Security Automation Portfolio

**Security-Focused AWS Automation**

Building practical cloud security tools and automation scripts using Python and AWS boto3.

---

## 👤 About

Cybersecurity professional with Security+ certification developing hands-on AWS security automation skills. This repository demonstrates practical cloud security knowledge through daily scripting challenges focused on:

- Security auditing and compliance
- Identity and Access Management (IAM)
- Infrastructure hardening
- Automated threat detection
- Incident response automation

---

## 🛠️ Technologies

- **Cloud Platform:** AWS (EC2, S3, IAM, CloudWatch, Lambda)
- **Language:** Python 3
- **SDK:** boto3
- **Tools:** AWS CLI, Git

---

## 📁 Projects

### Week 1: AWS Security Fundamentals

#### Day 1: S3 Bucket Enumeration
**Security Focus:** Asset discovery and inventory management
- Lists all S3 buckets in AWS account
- Identifies creation dates for audit trail
- Foundation for security compliance checks

#### Day 2: EC2 Instance Discovery
**Security Focus:** Compute resource inventory and monitoring
- Discovers all EC2 instances across account
- Tracks instance states and types
- Critical for attack surface management

#### Day 3: Instance Access Control
**Security Focus:** Incident response capability
- Start/stop EC2 instances programmatically
- Enables rapid containment during security incidents
- Demonstrates infrastructure control

#### Day 4: Secure Data Transfer
**Security Focus:** Data handling and encryption awareness
- Upload/download files to S3 securely
- Understanding of data-at-rest security
- Foundation for backup and recovery procedures

#### Day 5: IAM User Auditing
**Security Focus:** Identity and access management
- Audits all IAM users in organization
- Tracks password usage and account age
- Identifies dormant accounts (security risk)
- Supports least-privilege principle

---

## 🎯 Skills Demonstrated

- **Cloud Security:** AWS security best practices, compliance checking
- **Automation:** Python scripting for security operations
- **IAM:** User auditing, access control, least-privilege enforcement
- **Incident Response:** Rapid response automation, containment procedures
- **Compliance:** Security group audits, encryption verification
- **Monitoring:** CloudWatch integration, security alerting

---

## 🚀 Setup
```bash
# Clone repository
git clone https://github.com/CLARKYBOI/AWS-Python.git

# Install dependencies
pip install boto3

# Configure AWS credentials
aws configure
```

---

## 📝 Usage

Each script is standalone and can be run directly:
```bash
python day1_list_buckets.py
python day5_iam_user_lister.py
```

---

## 🔐 Security Considerations

- All scripts follow AWS security best practices
- Uses IAM roles and least-privilege access
- Implements error handling and input validation
- Includes dry-run capabilities where applicable

---

## 📚 Certifications

- **Security+** (CompTIA)
- **Bachelor's Degree:** Cybersecurity Technology

---

## 📫 Contact

Building cloud security skills one script at a time. Open to opportunities in:
- Cloud Security Engineering
- DevSecOps
- Security Operations (SOC)
- Compliance and Governance

---

## 📈 Progress

**Current:** Day 5 of 30
**Commits:** Building daily
**Focus:** Security automation and compliance
