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

```

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

### Modules 
### Main.tf

Defines the resource modules for the infrastructure:
- Resource Group: The resource_group module, sourced from resources/resource_group, creates a common resource group for AKS and ACR.
- AKS Cluster: The aks module, sourced from resources/aks, sets up the Azure Kubernetes Service cluster with key parameters like kubernetes_version, vm_size, and network_plugin. The AKS creation depends on the resource group.
- ACR: The acr module, sourced from resources/acr, deploys the Azure Container Registry. It depends on both the AKS and the resource group.

```bash
module "resource_group" {
  source = "../resources/resource_group"
  resource_group_name_acr = var.resource_group_name_acr
  location_acr = var.location_acr
}

module "aks" {
  source = "../resources/aks"
  resource_group_name_acr = module.resource_group.common_rg_name
  location = var.location
  cluster_name = var.cluster_name
  kubernetes_version = var.kubernetes_version
  system_node_count = var.system_node_count
  vm_size = var.vm_size
  zones = var.zones
  load_balancer_sku = var.load_balancer_sku
  network_plugin = var.network_plugin
  node_pool_type = var.node_pool_type
  identity_type = var.identity_type
  node_pool_name = var.node_pool_name
  depends_on = [module.resource_group]
}

module "acr" {
  source = "../resources/acr"
  resource_group_name_acr = module.resource_group.common_rg_name
  acr_name = var.acr_name
  location_acr = var.location_acr
  principal_id = module.aks.kubelet_identity
  depends_on = [module.resource_group, module.aks]
}
```
### Output.tf
This file defines the outputs from the deployed modules, including the resource group name and ID, ACR details, and AKS configurations (e.g., FQDN, node resource group).

```bash
output "resource_group_name" {
  value = module.resource_group.common_rg_name
}

output "resource_group_id" {
  value = module.resource_group.common_rg_id
}

output "acr_id" {
  value = module.acr.acr_id
}

output "acr_login_server" {
  value = module.acr.acr_login_server
}

output "aks_id" {
  value = module.aks.aks_id
}

output "aks_fqdn" {
  value = module.aks.aks_fqdn
}

output "aks_node_rg" {
  value = module.aks.aks_node_rg
}
```

### Provider.tf
Specifies the provider configuration for Azure. Ensure to update the subscription_id with your Azure subscription.
```bash
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
```

### Terraform.tfvars
 - Contains variable values that will be passed into the modules. It defines critical details like resource names, cluster configuration, and ACR setup.
```
resource_group_name_acr = "my-common-resource-group"
location = "Central India"
cluster_name = "AKSClusterdev"
kubernetes_version = "1.24.6"
system_node_count = 3
vm_size = "Standard_DS2_v2"
zones = [1, 2, 3]
load_balancer_sku = "standard"
network_plugin = "kubenet"
node_pool_type = "VirtualMachineScaleSets"
identity_type = "SystemAssigned"
acr_name = "acrdev"
location_acr = "Central India"
acr_sku = "Standard"
acr_admin_enabled = false
role_definition_name = "AcrPull"
skip_service_principal_aad_check = true
```
