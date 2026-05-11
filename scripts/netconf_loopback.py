from ncclient import manager
import os
import re

""" router_ip = os.getenv("ROUTER_IP")
username = os.getenv("ROUTER_USER")
password = os.getenv("ROUTER_PASS") """

""" router_ip = "192.168.56.105" """
router_ip = "172.17.3.1"
username = "manuel"
password = "student@pxl!"

print(f"Verbinden met {router_ip}")

with manager.connect(
    host=router_ip,
    port=830,
    username=username,
    password=password,
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:

    print("NETCONF verbinding succesvol")

    # 🔹 config laden
    with open("config/netconf_loopback.xml") as f:
        config = f.read()

    # 🔹 config toepassen
    print("Config pushen...")
    response = m.edit_config(target="running", config=config)
    print(response)

    # 🔹 verify (running config ophalen)
    print("\nVerificatie (running-config):")
    config_state = m.get_config(source="running")
    
    if re.search(r"Loopback\d{1,3}", config_state.data_xml):
        print("Loopback succesvol aanwezig!")
    else:
        print("Loopback NIET gevonden!")

print("Script volledig uitgevoerd")