<img width="940" height="374" alt="image" src="https://github.com/user-attachments/assets/bcb19acc-e742-4e1f-85d5-447a1803e993" />


# DevOps CI/CD Pipeline with Jenkins, SonarQube, and Docker

This project demonstrates a complete **DevOps CI/CD pipeline** using:

- **GitHub** → Code repository  
- **Jenkins** → CI/CD automation  
- **SonarQube** → Code quality analysis  
- **Docker** → Containerization and deployment  
- **Flask** → Simple Python web application  

---


## 📌 Project Structure

project10

│── app.py     # Flask application

│── requirements.txt  # Python dependencies

│── Dockerfile   # Docker image instructions

│── Jenkinsfile  # Jenkins pipeline configuration

│── README.md    # Project documentation



### 1. Prerequisites (what you need)

A machine (VM or cloud) running Ubuntu OR linux 20.04+ (or similar).

For SonarQube: ≥ 4 GB RAM recommended (2 GB minimum, but community features and Elasticsearch perform better with 4GB).

For Jenkins: 2+ GB recommended.

Installed tools on that machine (we’ll install them below): git, docker, docker-compose, java (for Jenkins), pip (optional).

A GitHub account and repository (you already have project10).

A SonarQube token (we’ll create SonarQube server locally and generate token).

Basic familiarity with terminal commands (I’ll include exact commands).

 ### Install git
   ```
   sudo yum update -y
   sudo yum install git -y
   git --version
   ```

### 2. Set up Docker (so we can run Jenkins & Sonar easily):

```
sudo yum install docker -y
```

```
sudo systemctl start docker
```

```
sudo docker pull sonarqube
sudo docker run -d -p 9000:9000 --name sonarqube sonarqube
```

### http://<your-server-ip>:9000

Default credentials: admin / admin (log in and change password).

### 3. Create a Sonar token:

### In Sonar UI: top-right → My Account → Security → Generate Token → name it e.g. jenkins-token. Copy token.

### 4. Install Jenkins (on same server )
```
sudo yum update –y
sudo yum install wget -y
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum upgrade -y
sudo dnf install java-21-amazon-corretto -y
sudo yum install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins  
```
Access Jenkins: http://<server-ip>:8080.
Follow initial unlock instructions (use the /var/lib/jenkins/secrets/initialAdminPassword).

Install recommended plugins when prompted (or install required ones later).

### 5. Install Jenkins plugins and tools

In Jenkins UI → Manage Jenkins → Manage Plugins:

### Install:

Git plugin

Pipeline stage view

Docker Pipeline

SonarQube Scanner for Jenkins

### 6. Configure SonarQube in Jenkins

**Manage Jenkins** → Configure System → SonarQube servers

**Add SonarQube:**

**Name:** SonarQube

**Server URL:** http://<server-ip>:9000

Server authentication token: enter token from Sonar UI (the jenkins-token) — click Add → Jenkins credential as secret text, give ID (optional).

Save.

**Manage Jenkins** → Global Tool Configuration → SonarQube Scanner

Add SonarQube Scanner installation:

**Name:** SonarScannerCLI

Optionally tick Install automatically (Jenkins will download scanner).

### 7. Add Sonar token as Jenkins Credential (best practice)

Manage Jenkins → Credentials → System → Global credentials → Add Credentials:

**Kind:** Secret text

**Secret:** <your-sonar-token>

**ID:** sonar-token

**save**

We’ll reference this in the pipeline.

### 8. Make sure Jenkins user can run Docker

If Jenkins runs on the same host and will build/run Docker images, add jenkins user to docker group:

```
sudo usermod -aG docker jenkins
```
Step 1 — Add Jenkins to Docker group

Run:
```
sudo usermod -aG docker jenkins
```
🔧 Step 2 — Restart services
```
sudo systemctl restart docker
sudo systemctl restart jenkins
```
🔧 Step 3 — Verify

Switch to jenkins user:
```
sudo su - jenkins
docker ps
```
Expected:
No permission error
Shows running containers or empty list
⚠️ If still failing

Run this to confirm group applied:

groups jenkins
Expected output:
jenkins docker
🔁 If NOT showing docker group

Run again:
```
sudo usermod -aG docker jenkins
sudo reboot
```
👉 Reboot ensures group membership is applied properly

🚫 Alternative (NOT recommended but quick test)

You can bypass permissions temporarily:
```
sudo chmod 666 /var/run/docker.sock
```
### 9. Create Jenkins Pipeline Job

### Jenkins → New Item → name project10-pipeline → Pipeline → OK.

### Pipeline → Definition: Pipeline script or Pipeline script from SCM.

If from SCM, choose Git, repo URL and Branch main, script path Jenkinsfile.

Save and Build Now.

### verify that your application is actually running and accessible.

### Go to:
**AWS Console → EC2 → Instances → Your instance → Security → Security Groups**

Add inbound rule:
Type: Custom TCP
Port: 5000
Source: 0.0.0.0/0

✔ Save the rule 

### 🎯 Step 1 — Check if container is running

On your Jenkins/EC2 server:
```
docker ps
```
✅ Expected output:

You should see your app container, something like:

my-devops-app   ...   0.0.0.0:5000->5000

👉 Important:

Container must be Up
Port mapping must exist (host_port:container_port)
### 🎯 Step 2 — Identify the port

From your docker run command (in Jenkinsfile), check:

Example:
```
docker run -d -p 5000:5000 my-devops-app
```
👉 This means:

App runs on port 5000
### 🎯 Step 3 — Test locally on server

Run:

curl http://localhost:5000

✅ Expected:
HTML response OR JSON response

👉 If this fails → app is not running correctly

🎯 Step 4 — Open in browser (important)

Use your EC2 public IP:

http://<your-ec2-public-ip>:5000
