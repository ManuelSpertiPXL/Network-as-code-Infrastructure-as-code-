# filters.py

def task18_if_stats():
    return """
    <filter type="subtree">
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>GigabitEthernet0/0/0</name>
          <statistics/>
        </interface>
      </interfaces-state>
    </filter>s
    """
def task28_routing():
    return """
    <filter>
      <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
      </routing-state>
    </filter>
    """
def get_interfaces_filter():
    return """
    <filter>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """

def get_running_filter():
    return None  # geen filter nodig


def get_routing_filter():
    return """
    <filter>
      <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
    </filter>
    """
def get_hostname():
    return """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
      </native>
    </filter>
    """

def get_motd_filter():
    return """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <motd>
            <banner/>
          </motd>
        </banner>
      </native>
    </filter>
    """
def get_hostname_and_interfaces():
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