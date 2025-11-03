output "prometheus_url" {
  description = "Prometheus server URL"
  value       = "https://${azurerm_container_app.prometheus.latest_revision_fqdn}"
}

output "grafana_url" {
  description = "Grafana dashboard URL"
  value       = "https://${azurerm_container_app.grafana.latest_revision_fqdn}"
}

output "grafana_credentials" {
  description = "Grafana login credentials"
  value = {
    username = "admin"
    password = var.grafana_admin_password
  }
  sensitive = true
}

output "monitoring_storage_account_name" {
  description = "Monitoring storage account name"
  value       = azurerm_storage_account.monitoring.name
}
