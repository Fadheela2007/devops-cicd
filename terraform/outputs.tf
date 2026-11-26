output "app_url" {
  description = "Adresse de l'application créée par Terraform"
  value       = "http://${var.vm_ip}:${var.external_port}"
}

output "container_id" {
  description = "Identifiant du conteneur"
  value       = docker_container.app_terraform.id
}
