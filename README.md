# Terraform Infrastructure for Azure AKS, ACR, and Resource Groups

This repository contains Infrastructure as Code (IaC) for deploying an Azure Resource Group, Azure Container Registry (ACR), and Azure Kubernetes Service (AKS) using Terraform and Azure CLI.

## Prerequisites
Before you can deploy the infrastructure, ensure that you have the following installed and configured:
- **Azure CLI**: To interact with Azure resources.
- **Terraform**: For infrastructure deployment. 
- **Azure Subscription**: You need an active Azure account with appropriate permissions.
 
Tools Used

Terraform: For infrastructure provisioning.

Azure CLI: To manage Azure resources and configure settings.

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
    ├── aks/
    │   ├── main.tf
    │   ├── output.tf
    │   ├── variables.tf
    ├── acr/
    │   ├── main.tf
    │   ├── output.tf
    │   ├── variables.tf
    ├── resource_group/
        ├── main.tf
        ├── output.tf
        ├── variables.tf


## Infrastructure Details

### Azure Resource Group
- All resources are grouped within a single resource group for better organization and management.
- The resource group configuration is located under `resources/resource_group/`.

### Azure Kubernetes Service (AKS)

- A fully managed Kubernetes cluster for running containerized applications.
- The AKS configuration is located under `resources/aks/` and is responsible for setting up the Kubernetes cluster with the specified node pools, networking configurations, and other relevant settings.

### Azure Container Registry (ACR)

- A private Docker registry used to store and manage container images.
- The ACR configuration is located under `resources/acr/`. Once deployed, you can push your container images to ACR for use in your AKS cluster.


