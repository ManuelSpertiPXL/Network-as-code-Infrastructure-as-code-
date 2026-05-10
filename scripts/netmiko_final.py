from netmiko import ConnectHandler
import os

router_ip = "40.113.133.31"
username = "cisco"
password = "cisco123!"

router = {
    "device_type": "cisco_ios",
    "host": router_ip,
    "username": username,
    "password": password,
}

print(f"🔌 Verbinden met {router['host']}")

connection = ConnectHandler(**router)

# 🔹 show command
output = connection.send_command("show ip interface brief")
print(output)

# 🔹 config toepassen
with open("config/netmiko_interface.txt") as f:
    commands = f.read().splitlines()

config_output = connection.send_config_set(commands)
print(config_output)

connection.disconnect()

print("✅ Netmiko script klaar")