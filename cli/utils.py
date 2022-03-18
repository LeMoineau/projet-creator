
from elements.channel import Channel

def get_node_type(node):
    return type(node).__name__ if not isinstance(node, Channel) else "Channel"