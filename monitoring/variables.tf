variable "project_name" {
  description = "Project name"
  type        = string
  default     = "gaming-forum"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "westus"
}

variable "resource_group_name" {
  description = "Existing resource group name"
  type        = string
}

variable "container_app_environment_id" {
  description = "Existing Container App Environment ID"
  type        = string
}

variable "backend_fqdn" {
  description = "Backend FQDN for Prometheus scraping"
  type        = string
}

variable "postgres_host" {
  description = "PostgreSQL server FQDN"
  type        = string
}

variable "postgres_user" {
  description = "PostgreSQL admin username"
  type        = string
}

variable "postgres_port" {
  description = "PostgreSQL server port"
  type        = number
  default     = 5432
}

variable "postgres_password" {
  description = "PostgreSQL admin password"
  type        = string
  sensitive   = true
}

variable "grafana_admin_password" {
  description = "Grafana admin password"
  type        = string
  default     = "GrafanaAdmin123!"
  sensitive   = true
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
