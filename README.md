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
## Variables.tf
 - Declares variables used throughout the modules. This includes configuration options for AKS, ACR, and the resource group.
```
variable "resource_group_name_acr" {
  description = "The name of the resource group"
  type = string
}

variable "location" {
  description = "Resources location in Azure"
  type = string
}

variable "location_acr" {
  description = "ACR location"
  type = string
}

variable "subscription_id" {
  description = "The subscription ID used for Azure."
  type = string
}

variable "cluster_name" {
  type = string
  description = "AKS name in Azure"
}

variable "kubernetes_version" {
  type = string
  description = "Kubernetes version"
}

variable "system_node_count" {
  type = number
  description = "Number of AKS worker nodes"
}

variable "vm_size" {
  description = "VM size for the AKS default node pool"
  type = string
  default = "Standard_DS2_v2"
}

variable "zones" {
  description = "Availability zones for AKS nodes"
  type = list(string)
  default = [1, 2, 3]
}

variable "load_balancer_sku" {
  description = "SKU of the Load Balancer for AKS"
  type = string
  default = "standard"
}

variable "network_plugin" {
  description = "Network plugin for AKS"
  type = string
  default = "kubenet"
}

variable "acr_name" {
  type = string
  description = "ACR name"
}

variable "acr_sku" {
  description = "SKU for the Azure Container Registry"
  type = string
  default = "Standard"
}

variable "acr_admin_enabled" {
  description = "Enable or disable admin access for the ACR"
  type = bool
  default = false
}

variable "role_definition_name" {
  description = "The name of the role definition for the role assignment"
  type = string
  default = "AcrPull"
}

variable "skip_service_principal_aad_check" {
  description = "Whether to skip the service principal AAD check"
  type = bool
  default = true
}

variable "node_pool_type" {
  description = "The type of the node pool (e.g., VirtualMachineScaleSets or AvailabilitySet)"
  type = string
  default = "VirtualMachineScaleSets"
}

variable "identity_type" {
  description = "The type of managed identity (e.g., SystemAssigned, UserAssigned)"
  type = string
  default = "SystemAssigned"
}

variable "node_pool_name" {
  description = "Name of the default node pool"
  type = string
  default = "system"
}
```
### Resource Group Module

This module creates an Azure Resource Group, which serves as a container for the other resources deployed (AKS and ACR).

#### `main.tf`

This file contains the resource definition for creating the Azure Resource Group.

```
resource "azurerm_resource_group" "common_rg" {
  name     = var.resource_group_name_acr
  location = var.location_acr
}
```
 - azurerm_resource_group: This resource creates a new Azure Resource Group.
 - name: The name of the resource group, sourced from the input variable resource_group_name_acr.
 - location: The Azure region where the resource group will be created, sourced from location_acr.

### Output.tf
 - This file defines the outputs from the Resource Group module.
```
   output "common_rg_name" {
  value       = azurerm_resource_group.common_rg.name
  description = "The name of the Azure resource group."
}

output "common_rg_id" {
  value       = azurerm_resource_group.common_rg.id
  description = "The ID of the Azure resource group."
}
```
### Outputs:
  - common_rg_name: Outputs the name of the created resource group.
  - common_rg_id: Outputs the ID of the created resource group, which can be used for referencing this resource in other configurations.

### Variable.tf
  - This file declares the input variables required by the Resource Group module.
```
variable "resource_group_name_acr" {
  description = "The name of the resource group"
  type        = string
}

variable "location_acr" {
  description = "The location of the resource group"
  type        = string
}
```

### Azure Kubernetes Service (AKS) Module

 - This module sets up an Azure Kubernetes Service (AKS) cluster, which is a managed container orchestration service.

#### `Main.tf`

 - This file contains the resource definition for creating the AKS cluster.

```hcl
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  kubernetes_version  = var.kubernetes_version
  location            = var.location
  resource_group_name = var.resource_group_name_acr  # Reference the same resource group
  dns_prefix          = var.cluster_name

  default_node_pool {
    name       = var.node_pool_name 
    node_count = var.system_node_count             # From terraform.tfvars
    vm_size    = var.vm_size                       # From terraform.tfvars
    type       = var.node_pool_type         # Fixed type
    zones      = var.zones                         # From terraform.tfvars
  }

  identity {
    type = var.identity_type
  }

  network_profile {
    load_balancer_sku = var.load_balancer_sku      # From terraform.tfvars
    network_plugin    = var.network_plugin         # From terraform.tfvars
  }
}
```

 - azurerm_kubernetes_cluster: This resource defines the AKS cluster.
 - name: Name of the AKS cluster, sourced from the variable cluster_name.
 - kubernetes_version: Version of Kubernetes to use, sourced from kubernetes_version.
 - location: Azure region where the AKS cluster will be created.
 - resource_group_name: The resource group where the AKS will be deployed.
 - dns_prefix: DNS prefix for the AKS cluster.
 - Default Node Pool: Specifies the configuration for the default node pool, including:
 - name: Name of the node pool.
 - node_count: Number of worker nodes.
 - vm_size: Size of the virtual machines.
 - type: Type of the node pool.
 - zones: Availability zones for the AKS nodes.
 - Identity: Defines the managed identity type for the AKS cluster.
 - Network Profile: Configures the network settings for the AKS cluster.

### Output.tf
 - This file defines the outputs from the AKS module.
```
output "aks_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "aks_fqdn" {
  value = azurerm_kubernetes_cluster.aks.fqdn
}

output "aks_node_rg" {
  value = azurerm_kubernetes_cluster.aks.node_resource_group
}

output "kubelet_identity" {
  value = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}
```
## Outputs:

 - aks_id: Outputs the ID of the created AKS cluster.
 - aks_fqdn: Outputs the fully qualified domain name of the AKS cluster.
 - aks_node_rg: Outputs the resource group where the AKS nodes are located.
 - kubelet_identity: Outputs the object ID of the kubelet identity.
   
###Variable.tf
 - This file declares the input variables required by the AKS module.
```
variable "resource_group_name_acr" {
  description = "The name of the resource group where the ACR is deployed"
  type        = string
}

variable "location" {
  type        = string
  description = "Resources location in Azure"
}

variable "cluster_name" {
  type        = string
  description = "AKS name in Azure"
}

variable "kubernetes_version" {
  type        = string
  description = "Kubernetes version"
}

variable "system_node_count" {
  type        = number
  description = "Number of AKS worker nodes"
}

variable "vm_size" {
  description = "VM size for the AKS default node pool"
  type        = string
  default     = "Standard_DS2_v2"  # Optional default value
}

variable "zones" {
  description = "Availability zones for AKS nodes"
  type        = list(string)
  default     = [1, 2, 3]  # Optional default value for zones
}

variable "load_balancer_sku" {
  description = "SKU of the Load Balancer for AKS"
  type        = string
  default     = "standard"  # Optional default value
}

variable "network_plugin" {
  description = "Network plugin for AKS"
  type        = string
  default     = "kubenet"  # Optional default value
}

variable "identity_type" {
  description = "The type of managed identity (e.g., SystemAssigned, UserAssigned)"
  type        = string
  default     = "SystemAssigned"  # Default value is set to "SystemAssigned"
}

variable "node_pool_type" {
  description = "The type of the node pool (e.g., VirtualMachineScaleSets or AvailabilitySet)"
  type        = string
  default     = "VirtualMachineScaleSets"  # Default value is set to "VirtualMachineScaleSets"
}

variable "node_pool_name" {
  description = "Name of the default node pool"
  type        = string
  default     = "system"  # Optional: Set a default value to 'system', if that is commonly used
}
```
### Variables
 - resource_group_name_acr: The name of the resource group where the ACR is deployed.
 - location: The Azure region for resource deployment.
 - cluster_name: The name of the AKS cluster.
 - kubernetes_version: The version of Kubernetes to deploy.
 - system_node_count: The number of worker nodes in the AKS cluster.
 - vm_size: The size of the virtual machines in the node pool.
 - zones: Availability zones for the AKS nodes.
 - load_balancer_sku: SKU for the load balancer.
 - network_plugin: Network plugin configuration.
 - identity_type: Type of managed identity for the AKS.
 - node_pool_type: Type of the node pool (VirtualMachineScaleSets or AvailabilitySet).
 - node_pool_name: Name of the default node pool.



### Azure Container Registry (ACR) Module

This module sets up an Azure Container Registry (ACR), which is a private Docker registry used to store and manage container images.

#### `Main.tf`

 - This file contains the resource definitions for creating the ACR and assigning roles.

```hcl
resource "azurerm_container_registry" "acr" { 
  name                = var.acr_name
  resource_group_name = var.resource_group_name_acr  # Use the variable for the resource group
  location            = var.location_acr
  sku                 = var.acr_sku                # Use variable for SKU
  admin_enabled       = var.acr_admin_enabled       # Use variable for admin access
}

resource "azurerm_role_assignment" "role_acrpull" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = var.role_definition_name             # Use variable for role definition
  principal_id                     = var.principal_id  # Use the variable for principal_id
  skip_service_principal_aad_check = var.skip_service_principal_aad_check # Use variable for skipping AAD check
}
```
 - azurerm_container_registry: This resource defines the Azure Container Registry.
 - name: The name of the ACR, sourced from the variable acr_name.
 - resource_group_name: The resource group where the ACR will be deployed.
 - location: Azure region for the ACR deployment.
 - sku: The SKU (pricing tier) for the ACR, sourced from acr_sku.
 - admin_enabled: Whether admin access is enabled for the ACR.
 - azurerm_role_assignment: This resource assigns a role to a principal to access the ACR.

 - scope: The scope of the role assignment, referencing the ACR ID.
 - role_definition_name: The name of the role definition, sourced from role_definition_name.
 - principal_id: The object ID of the principal (e.g., AKS kubelet identity) that will have the role assigned.
 - skip_service_principal_aad_check: Indicates whether to skip the AAD check for the service principal.

###Output.tf
 - This file defines the outputs from the ACR module.
```
output "acr_id" {
  value = azurerm_container_registry.acr.id
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}
```
Outputs:
 - acr_id: Outputs the ID of the created ACR.
 - acr_login_server: Outputs the login server URL for the ACR.

###Variable.tf
 - This file declares the input variables required by the ACR module.
```
variable "acr_name" {
  type        = string
  description = "ACR name"
}

variable "location_acr" {
  type        = string
  description = "ACR location"
}

variable "resource_group_name_acr" {
  type        = string
  description = "Resource group name for ACR"
}

variable "acr_sku" {
  description = "SKU for the Azure Container Registry"
  type        = string
  default     = "Standard"  # Default value for ACR SKU
}

variable "acr_admin_enabled" {
  description = "Enable or disable admin access for the ACR"
  type        = bool
  default     = false  # Default value for admin access
}

variable "role_definition_name" {
  description = "The name of the role definition for the role assignment"
  type        = string
  default     = "AcrPull"  # Default value for role definition name
}

variable "skip_service_principal_aad_check" {
  description = "Whether to skip the service principal AAD check"
  type        = bool
  default     = true  # Default value for skipping the AAD check
}

variable "principal_id" {
  type        = string
  description = "The object ID of the AKS kubelet identity"
}
```
### Variables
 - acr_name: The name of the Azure Container Registry.
 - location_acr: The Azure region for the ACR deployment.
 - resource_group_name_acr: The name of the resource group where the ACR will be deployed.
 - acr_sku: The SKU for the ACR.
 - acr_admin_enabled: Indicates if admin access is enabled for the ACR.
 - role_definition_name: The name of the role for the assignment.
 - skip_service_principal_aad_check: Indicates whether to skip the AAD check for service principal.
 - principal_id: The object ID of the AKS kubelet identity.
