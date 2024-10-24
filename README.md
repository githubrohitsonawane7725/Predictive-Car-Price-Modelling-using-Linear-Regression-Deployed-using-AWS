# Terraform Infrastructure for Azure AKS, ACR, and Resource Groups

This repository contains Infrastructure as Code (IaC) for deploying an Azure Resource Group, Azure Container Registry (ACR), and Azure Kubernetes Service (AKS) using Terraform and Azure CLI.

## Directory Structure

```bash
IAC-using-terraform/
├── modules/
│   ├── main.tf
│   ├── output.tf
│   ├── provider.tf
│   ├── terraform.tfvars
│   ├── variables.tf
├── resources/
│   ├── aks/
│   │   ├── main.tf
│   │   ├── output.tf
│   │   ├── variables.tf
│   ├── acr/
│   │   ├── main.tf
│   │   ├── output.tf
│   │   ├── variables.tf
│   ├── resource_group/
│   │   ├── main.tf
│   │   ├── output.tf
│   │   ├── variables.tf

