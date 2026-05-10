from netmiko import ConnectHandler
import os

router = {
    "device_type": "cisco_ios",
    "host": os.getenv("AZ_ROUTER_IP"),
    "username": os.getenv("AZ_ROUTER_USER"),
    "password": os.getenv("AZ_ROUTER_PASS"),
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