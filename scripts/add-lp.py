from ncclient import manager
import os

def load_xml():
    base = os.path.dirname(__file__)
    path = os.path.join(base, "..", "config", "netconf_lb.xml")

    with open(path, "r") as f:
        return f.read()

def push_config():
    payload = load_xml()

    print("=== PAYLOAD ===")
    print(payload)
    print("===============")

    with manager.connect(
        host="192.168.56.105",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False,
        device_params={"name": "iosxe"}
    ) as m:

        print("Connected")

        response = m.edit_config(
            target="running",
            config=payload
        )

        print("DONE")
        print(response)

if __name__ == "__main__":
    push_config()
