terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.2.0"
    }
  }

  cloud {
    organization = "sambeth"

    workspaces {
      name = "github-actions"
    }
  }
}
provider "aws" {
  region = "us-east-2"
}
