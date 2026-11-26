variable "vm_ip" {
  description = "Adresse IP de la VM Vagrant"
  type        = string
  default     = "192.168.56.10"
}

variable "container_name" {
  description = "Nom du conteneur créé par Terraform"
  type        = string
  default     = "app-terraform"
}

variable "external_port" {
  description = "Port exposé sur la VM"
  type        = number
  default     = 8081
}
