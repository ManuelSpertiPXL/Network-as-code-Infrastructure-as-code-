# filters.py

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
def get_hostname_filter():
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