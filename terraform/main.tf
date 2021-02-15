# terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.5.0"
    }
  }
}

provider "azurerm" {
  client_id       = var.client_id
  client_secret   = var.client_secret
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id

  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-aks-rg"
  location = var.location
}

terraform {
  backend "azurerm" {
    resource_group_name  = "resourceGroupName"
    storage_account_name = "sociallmetstate19713"
    container_name       = "identitytstate"
    key                  = "terraform.tfstate"
    access_key           = "nO6UuIU0vYA=="
  }
}

# Azure Blob Storage
resource "azurerm_storage_account" "identitystorage" {
  name                     = "identitystorageacc"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "identitymedia" {
  name                  = "media"
  storage_account_name  = azurerm_storage_account.identitystorage.name
  container_access_type = "blob"
}

resource "azurerm_storage_container" "identitystatic" {
  name                  = "static"
  storage_account_name  = azurerm_storage_account.identitystorage.name
  container_access_type = "blob"
}

# resource "azurerm_storage_blob" "example" {
#   name                   = "my-awesome-content.zip"
#   storage_account_name   = azurerm_storage_account.example.name
#   storage_container_name = azurerm_storage_container.example.name
#   type                   = "Block"
#   source                 = "some-local-file.zip"
# }
# End of Azure Blob Storage

# Create Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "${var.acr-prefix}acr"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
  admin_enabled       = "true"
}

resource "azurerm_virtual_network" "vn" {
  name                = "${var.prefix}-Vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["192.168.0.0/16"]
}

resource "azurerm_subnet" "subnet" {
  name                 = "${var.prefix}-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  address_prefix       = "192.168.1.0/24"
  virtual_network_name = azurerm_virtual_network.vn.name
  service_endpoints    = ["Microsoft.Sql"]
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.prefix}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.prefix}-dns"
  kubernetes_version  = "1.19.0"

  default_node_pool {
    name            = "scoialmepool" # Must be lowercase and max 12 chars
    node_count      = 3
    vm_size         = "Standard_D2_v2"
    os_disk_size_gb = 30
    vnet_subnet_id  = azurerm_subnet.subnet.id
  }

  network_profile {
    network_plugin    = "kubenet"
    load_balancer_sku = "Standard"
  }

  service_principal {
    client_id     = var.client_id
    client_secret = var.client_secret
  }
}

data "azurerm_public_ip" "pip" {
  name                = reverse(split("/", tolist(azurerm_kubernetes_cluster.aks.network_profile.0.load_balancer_profile.0.effective_outbound_ips)[0]))[0]
  resource_group_name = azurerm_kubernetes_cluster.aks.node_resource_group
}
