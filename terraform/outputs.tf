output "resource_group_name" {
  description = "Resource Group name"
  value       = azurerm_resource_group.main.name
}

output "location" {
  description = "Azure region"
  value       = azurerm_resource_group.main.location
}

output "acr_login_server" {
  description = "Container Registry login server"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_name" {
  description = "Container Registry name"
  value       = azurerm_container_registry.acr.name
}

output "acr_username" {
  description = "Container Registry admin username"
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
}

output "acr_password" {
  description = "Container Registry admin password"
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "database_fqdn" {
  description = "PostgreSQL server FQDN"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "database_name" {
  description = "PostgreSQL database name"
  value       = azurerm_postgresql_flexible_server_database.main.name
}

output "database_connection_string" {
  description = "PostgreSQL connection string (sensitive)"
  value       = "postgresql://${var.db_admin_username}:${var.db_admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/forum_db?sslmode=require"
  sensitive   = true
}

output "container_app_environment_id" {
  description = "Container Apps Environment ID"
  value       = azurerm_container_app_environment.main.id
}

output "container_app_environment_name" {
  description = "Container Apps Environment name"
  value       = azurerm_container_app_environment.main.name
}

# For CircleCI
output "deployment_info" {
  description = "Information needed for CircleCI deployment"
  value = {
    resource_group      = azurerm_resource_group.main.name
    acr_login_server    = azurerm_container_registry.acr.login_server
    environment_name    = azurerm_container_app_environment.main.name
    database_fqdn       = azurerm_postgresql_flexible_server.main.fqdn
    location            = azurerm_resource_group.main.location
  }
}

