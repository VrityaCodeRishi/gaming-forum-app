variable "project_name" {
  description = "Project name (used in resource naming)"
  type        = string
  default     = "gaming-forum"
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "prod"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus"
}

variable "db_admin_username" {
  description = "PostgreSQL administrator username"
  type        = string
  default     = "pgadmin"
  
  validation {
    condition     = length(var.db_admin_username) >= 3 && length(var.db_admin_username) <= 63
    error_message = "Username must be between 3 and 63 characters."
  }
}

variable "db_admin_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
  
  validation {
    condition     = length(var.db_admin_password) >= 8
    error_message = "Password must be at least 8 characters long."
  }
}
