from netmiko import ConnectHandler
import os
import paramiko
from datetime import datetime


# ✅ forceer oude SSH settings
paramiko.transport.Transport._preferred_kex = (
    "diffie-hellman-group14-sha1",
    "diffie-hellman-group1-sha1",
)

paramiko.transport.Transport._preferred_keys = (
    "ssh-rsa",
)

# 🔹 meerdere routers (kan je uitbreiden)
routers = [
    {
        "device_type": "cisco_ios",
        "host": os.getenv("AZ_ROUTER_IP"),
        "username": os.getenv("AZ_ROUTER_USER"),
        "password": os.getenv("AZ_ROUTER_PASS"),
        "fast_cli": False
    }
]

# 🔹 functie: backup maken
def backup_config(connection, host):
    print(f"[+] Backup maken voor {host}")
    
    running_config = connection.send_command("show running-config")

    # timestamp voor uniek bestand
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"backups/{host}_{timestamp}.txt"

    os.makedirs("backups", exist_ok=True)

    with open(filename, "w") as f:
        f.write(running_config)

    print(f"[+] Backup opgeslagen in {filename}")


# 🔹 functie: config toepassen
def apply_config(connection):
    print("[+] Config laden uit file")

    with open("config/interface.txt") as f:
        commands = f.read().splitlines()

    output = connection.send_config_set(commands)
    print(output)


# 🔹 functie: verificatie
def verify_config(connection):
    print("[+] Config controleren")

    output = connection.send_command("show ip interface brief")

    if "GigabitEthernet1" in output:
        print("[✅] Interface gevonden")
    else:
        print("[❌] Interface NIET gevonden")


# 🔹 MAIN SCRIPT
def main():
    for router in routers:
        try:
            print(f"\n🔌 Verbinden met {router['host']}")

            connection = ConnectHandler(**router)

            print("[+] Verbonden")

            # 1️⃣ backup
            backup_config(connection, router["host"])

            # 2️⃣ config push
            apply_config(connection)

            # 3️⃣ verificatie
            verify_config(connection)

            connection.disconnect()
            print("[+] Verbinding gesloten")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()