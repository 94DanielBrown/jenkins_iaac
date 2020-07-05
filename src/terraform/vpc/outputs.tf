output "vpc_id_out" {
  value = aws_vpc.main.id
}

output "subnet_id_out" {
  value = aws_subnet.public.id
}
