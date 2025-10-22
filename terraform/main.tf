# Azure Container Instances for Trading Bot
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "trading_bot" {
  name     = "rg-alpaca-trading-bot"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "AlpacaTradingBot"
    ManagedBy   = "Terraform"
  }
}

# Container Registry
resource "azurerm_container_registry" "trading_bot" {
  name                = "acralpacabot${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.trading_bot.name
  location           = azurerm_resource_group.trading_bot.location
  sku                = "Standard"
  admin_enabled      = true

  tags = {
    Environment = var.environment
    Project     = "AlpacaTradingBot"
  }
}

# Key Vault for secrets
resource "azurerm_key_vault" "trading_bot" {
  name                = "kv-alpaca-bot-${random_string.suffix.result}"
  location           = azurerm_resource_group.trading_bot.location
  resource_group_name = azurerm_resource_group.trading_bot.name
  tenant_id          = data.azurerm_client_config.current.tenant_id
  sku_name           = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Recover", "Backup", "Restore"
    ]
  }
}

# Container Instance
resource "azurerm_container_group" "trading_bot" {
  name                = "aci-alpaca-trading-bot"
  location           = azurerm_resource_group.trading_bot.location
  resource_group_name = azurerm_resource_group.trading_bot.name
  os_type            = "Linux"
  restart_policy     = "Always"

  container {
    name   = "trading-bot"
    image  = "${azurerm_container_registry.trading_bot.login_server}/alpaca-trading-bot:latest"
    cpu    = "0.5"
    memory = "1.0"

    ports {
      port     = 8080
      protocol = "TCP"
    }

    environment_variables = {
      PYTHONUNBUFFERED = "1"
      ENVIRONMENT      = var.environment
    }
  }

  image_registry_credential {
    server   = azurerm_container_registry.trading_bot.login_server
    username = azurerm_container_registry.trading_bot.admin_username
    password = azurerm_container_registry.trading_bot.admin_password
  }

  tags = {
    Environment = var.environment
    Project     = "AlpacaTradingBot"
  }
}

# Random string for unique names
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Data sources
data "azurerm_client_config" "current" {}

# Variables
variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# Outputs
output "container_registry_login_server" {
  value = azurerm_container_registry.trading_bot.login_server
}

output "container_instance_ip" {
  value = azurerm_container_group.trading_bot.ip_address
}

output "key_vault_uri" {
  value = azurerm_key_vault.trading_bot.vault_uri
}