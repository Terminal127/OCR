#!/bin/bash
sudo apt update 
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo usermod -aG docker ubuntu
sudo hostnamectl set-hostname Jenkins
sudo apt install openjdk-17-jdk -y
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo gpg --dearmor -o /usr/share/keyrings/jenkins-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.gpg] https://pkg.jenkins.io/debian binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins -y
sudo systemctl start jenkins
sh -c "sudo cat /var/lib/jenkins/secrets/initialAdminPassword >> ~/jenkins_initial_admin_password.txt"
sh -c "echo "Jenkins installation script completed. Initial admin password saved to ~/jenkins_initial_admin_password.txt.""
