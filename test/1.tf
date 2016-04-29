variable "foo" {
    default = "foo-default"
}

output "foo-out" {
    value = "${var.foo}"
}
