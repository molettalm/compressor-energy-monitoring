terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.52.0"
    }
  }
}

provider "azurerm" {
   features {}
}

resource "azurerm_resource_group" "main" {
  name     = "projeto_integrador_2"
  location = "South Central US"
}


resource "azurerm_mysql_flexible_server" "main" {
  name                   = "utfpr-pi2-compressor-monitor"
  resource_group_name    = azurerm_resource_group.main.name
  location               = "North Central US"
  administrator_login    = "pi2root"
  administrator_password = "UTFPR@senha"
  backup_retention_days  = 7
  sku_name               = "B_Standard_B1ms"
  version = "8.0.21"
  storage {
	auto_grow_enabled  = false
  }
}


resource "azurerm_mysql_flexible_server_firewall_rule" "main" {
  name                = "AllowAll"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.main.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}

resource "azurerm_mysql_flexible_database" "main" {
  name                = "pi2"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.main.name
  charset             = "utf8"
  collation           = "utf8_unicode_ci"
}

resource "azurerm_mysql_flexible_server_configuration" "main" {
  name                = "require_secure_transport"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_mysql_flexible_server.main.name
  value               = "OFF"
}
