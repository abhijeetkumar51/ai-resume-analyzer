# Terraform starter

`render.yaml` is the source of truth for this Render web service, including its Docker build and `/health` probe. This folder is intentionally a safe Terraform starting point rather than a pretend Render host configuration. Render manages the service runtime; its web-service plan does not give this project SSH or host-level access.

Use Terraform later for external infrastructure you control (for example DNS or a separately hosted monitoring server). Pin provider versions, use remote state where appropriate, and provide credentials through environment variables or a secrets manager. Do not commit state files or secrets.
