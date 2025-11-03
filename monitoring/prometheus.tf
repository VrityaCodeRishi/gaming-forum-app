# File Share for Prometheus Config
resource "azurerm_storage_share" "prometheus_config" {
  name                 = "prometheus-config"
  storage_account_name = azurerm_storage_account.monitoring.name
  quota                = 1

  depends_on = [time_sleep.storage_account_ready]
}

# Generate Prometheus config from template
locals {
  prometheus_config = templatefile("${path.module}/config/prometheus.yml.tpl", {
    backend_fqdn = var.backend_fqdn
  })
}

# Write config to local file
resource "local_file" "prometheus_yml" {
  content  = local.prometheus_config
  filename = "${path.module}/.generated/prometheus.yml"
}

# Upload Prometheus Config
resource "azurerm_storage_share_file" "prometheus_yml" {
  name             = "prometheus.yml"
  storage_share_id = azurerm_storage_share.prometheus_config.id
  source           = local_file.prometheus_yml.filename

  depends_on = [local_file.prometheus_yml]
}

# Container App Environment Storage
resource "azurerm_container_app_environment_storage" "prometheus_config" {
  name                         = "prometheus-config"
  container_app_environment_id = var.container_app_environment_id
  account_name                 = azurerm_storage_account.monitoring.name
  share_name                   = azurerm_storage_share.prometheus_config.name
  access_key                   = azurerm_storage_account.monitoring.primary_access_key
  access_mode                  = "ReadOnly"
}

# Prometheus Container App
resource "azurerm_container_app" "prometheus" {
  name                         = "${local.name_prefix}-prometheus"
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = "prometheus"
      image  = "prom/prometheus:latest"
      cpu    = 0.5
      memory = "1Gi"

      args = [
        "--config.file=/etc/prometheus/prometheus.yml",
        "--storage.tsdb.path=/prometheus",
        "--storage.tsdb.retention.time=15d",
        "--web.enable-lifecycle"
      ]

      volume_mounts {
        name = "prometheus-config"
        path = "/etc/prometheus"
      }
    }

    volume {
      name         = "prometheus-config"
      storage_type = "AzureFile"
      storage_name = azurerm_container_app_environment_storage.prometheus_config.name
    }

    min_replicas = 1
    max_replicas = 1
  }

  ingress {
    external_enabled = true
    target_port      = 9090

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  tags = local.common_tags
}
