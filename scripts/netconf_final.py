from ncclient import manager
import os

""" router_ip = "40.113.133.31"
username = "cisco"
password = "cisco123!" """

router_ip = os.getenv("AZ_ROUTER_IP")
username = os.getenv("AZ_ROUTER_USER")
password = os.getenv("AZ_ROUTER_PASS")

print(f"🔌 Verbinden met {router_ip}")

with manager.connect(
    host=router_ip,
    port=830,
    username=username,
    password=password,
    hostkey_verify=False
) as m:

    print("✅ NETCONF verbinding succesvol")

    # config laden
    with open("config/netconf_interface.xml") as f:
        config = f.read()

    # config pushen
    response = m.edit_config(target="running", config=config)
    print(response)

print("✅ NETCONF script klaar")