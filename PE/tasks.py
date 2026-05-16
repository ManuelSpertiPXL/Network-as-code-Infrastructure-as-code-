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
def task2_interface_enable():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <shutdown>false</shutdown>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task3_set_ipv4():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>1</name>
            <ip>
              <address>
                <primary>
                  <address>192.168.1.1</address>
                  <mask>255.255.255.0</mask>
                </primary>
              </address>
            </ip>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task4_remove_ipv4():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet operation="merge">
            <name>1</name>
            <ip operation="delete"/>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """
def task5_create_loopback():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>10</name>
          </Loopback>
        </interface>
      </native>
    </config>
    """
def task6_loopback_ip():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>10</name>
            <ip>
              <address>
                <primary>
                  <address>10.10.10.1</address>
                  <mask>255.255.255.255</mask>
                </primary>
              </address>
            </ip>
          </Loopback>
        </interface>
      </native>
    </config>
    """
def task7_hostname():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>NETCONF-Router</hostname>
      </native>
    </config>
    """
def task8_dns():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <name-server>8.8.8.8</name-server>
        </ip>
      </native>
    </config>
    """
def task9_ntp():
    return """
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ntp>
          <server>
            <server-list>
              <ip-address>192.168.1.100</ip-address>
            </server-list>
          </server>
        </ntp>
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
              <prefix>10.0.0.0</prefix>
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

def get_interfaces_and_hostname():
    return """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
      </native>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name/>
          <enabled/>
        </interface>
      </interfaces>
    </filter>
    """

def task18_get_interface_stats():
    return """
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name/>
          <statistics/>
        </interface>
      </interfaces-state>
    </filter>
    """