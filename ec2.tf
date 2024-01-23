//the basic initialization code
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

// the code for the provider
provider "aws" {
  region     = "ap-south-1"
  access_key = "AKIAYQEO4SWROPSCLV57"
  secret_key = "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"
  # Configuration options
}

# RSA key of size 4096 bits
resource "tls_private_key" "rsa_1024" {
  algorithm = "RSA"
  rsa_bits  = 1024
}

#keypair for the ec2 instance
resource "aws_key_pair" "key_pair" {
  key_name   = "deployer-key"
  public_key = "${tls_private_key.rsa_1024.public_key_openssh}"
}
//saving resources
resource "local_file" "private_key" {
  content  = "${tls_private_key.rsa_1024.private_key_pem}"
  filename = "private_key.pem"
}

//creating a instance with t2.micro
resource "aws_instance" "web" {
  ami                    = "ami-03f4878755434977f"
  instance_type          = "t2.micro"
  count                  = 1
  key_name               = aws_key_pair.key_pair.key_name
  user_data              = file("jenkins.sh")
  vpc_security_group_ids = ["${aws_security_group.allow_tls.id}"]
  tags = {
    Name = "jenkins"
  }
}

//creating a instance with t2.medium
# resource "aws_instance" "db" {
#   ami                    = "ami-03f4878755434977f"
#   instance_type          = "t2.medium"
#   count                  = 1
#   key_name               = aws_key_pair.key_pair.key_name
#   user_data              = file("kubernetes.sh")
#   vpc_security_group_ids = ["${aws_security_group.allow_tls.id}"]
#   tags = {
#     Name = "kubernetes"
#   }
# }

#security
resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"

    ingress {
      description = "TLS from VPC"
      from_port   = 0
      to_port     = 65535
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
   egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }


}

