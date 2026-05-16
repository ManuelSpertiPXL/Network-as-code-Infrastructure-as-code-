def task7_hostname():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>NETCONF-LAB</hostname>
      </native>
    </config>
    """


def task1_interface_description():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <description>Configured via NETCONF</description>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """


def task10_static_route():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <route>
            <ip-route-interface-forwarding-list>
              <prefix>10.10.10.0</prefix>
              <mask>255.255.255.0</mask>
              <fwd-list>
                <fwd>192.168.1.254</fwd>
              </fwd-list>
            </ip-route-interface-forwarding-list>
          </route>
        </ip>
      </native>
    </config>
    """
def set_hostname():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>HULK</hostname>
      </native>
    </config>
    """