terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "app_network" {
  name = "tf-tasktracker-net"
}

resource "docker_image" "redis" {
  name = "redis:7-alpine"
}

resource "docker_container" "redis" {
  name  = "tf-redis"
  image = docker_image.redis.image_id
  networks_advanced {
    name = docker_network.app_network.name
  }
}

resource "docker_image" "web" {
  name = "task-tracker-web:latest"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "tf-web"
  image = docker_image.web.image_id
  ports {
    internal = 5000
    external = 5002
  }
  env = ["REDIS_HOST=tf-redis"]
  networks_advanced {
    name = docker_network.app_network.name
  }
  depends_on = [docker_container.redis]
}
