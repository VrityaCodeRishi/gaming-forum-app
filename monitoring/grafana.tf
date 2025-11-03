# File Share for Grafana Provisioning
resource "azurerm_storage_share" "grafana_provisioning" {
  name                 = "grafana-provisioning"
  storage_account_name = azurerm_storage_account.monitoring.name
  quota                = 1

  depends_on = [time_sleep.storage_account_ready]
}

resource "azurerm_storage_share_directory" "grafana_datasources" {
  name             = "datasources"
  storage_share_id = azurerm_storage_share.grafana_provisioning.id
}

# Generate Grafana datasources config
locals {
  grafana_postgres_url = (
    startswith(var.postgres_host, "postgresql://")
    ? var.postgres_host
    : (
      length(regexall(":[0-9]+$", var.postgres_host)) > 0
      ? var.postgres_host
      : "${var.postgres_host}:${var.postgres_port}"
    )
  )

  grafana_datasources = templatefile("${path.module}/config/grafana-datasources.yml.tpl", {
    prometheus_fqdn   = azurerm_container_app.prometheus.latest_revision_fqdn
    postgres_url      = local.grafana_postgres_url
    postgres_user     = var.postgres_user
    postgres_password = var.postgres_password
  })
}

# Write config to local file
resource "local_file" "grafana_datasources" {
  content  = local.grafana_datasources
  filename = "${path.module}/.generated/datasources.yml"
}

# Upload Grafana datasources config
resource "azurerm_storage_share_file" "grafana_datasources" {
  name             = "datasources.yml"
  path             = "datasources"
  storage_share_id = azurerm_storage_share.grafana_provisioning.id
  source           = local_file.grafana_datasources.filename

  depends_on = [
    local_file.grafana_datasources,
    azurerm_storage_share_directory.grafana_datasources,
  ]
}

# Container App Environment Storage
resource "azurerm_container_app_environment_storage" "grafana_provisioning" {
  name                         = "grafana-provisioning"
  container_app_environment_id = var.container_app_environment_id
  account_name                 = azurerm_storage_account.monitoring.name
  share_name                   = azurerm_storage_share.grafana_provisioning.name
  access_key                   = azurerm_storage_account.monitoring.primary_access_key
  access_mode                  = "ReadWrite"
}

# Grafana Container App
resource "azurerm_container_app" "grafana" {
  name                         = "${local.name_prefix}-grafana"
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    container {
      name   = "grafana"
      image  = "grafana/grafana:latest"
      cpu    = 0.75
      memory = "1.5Gi"

      env {
        name  = "GF_SECURITY_ADMIN_USER"
        value = "admin"
      }

      env {
        name  = "GF_SECURITY_ADMIN_PASSWORD"
        value = var.grafana_admin_password
      }

      env {
        name  = "GF_SERVER_ROOT_URL"
        value = "https://%(domain)s/"
      }

      env {
        name  = "GF_AUTH_ANONYMOUS_ENABLED"
        value = "true"
      }

      env {
        name  = "GF_AUTH_ANONYMOUS_ORG_ROLE"
        value = "Viewer"
      }

      env {
        name  = "GF_USERS_ALLOW_SIGN_UP"
        value = "false"
      }

      env {
        name  = "GF_PATHS_PROVISIONING"
        value = "/etc/grafana/provisioning"
      }

      env {
        name  = "GF_LOG_LEVEL"
        value = "debug"
      }

      volume_mounts {
        name = "grafana-provisioning"
        path = "/etc/grafana/provisioning"
      }
    }

    volume {
      name         = "grafana-provisioning"
      storage_type = "AzureFile"
      storage_name = azurerm_container_app_environment_storage.grafana_provisioning.name
    }

    min_replicas = 1
    max_replicas = 1
  }

  ingress {
    external_enabled = true
    target_port      = 3000

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  tags = local.common_tags

  depends_on = [
    azurerm_container_app.prometheus,
    azurerm_storage_share_file.grafana_datasources
  ]
}
