class Node:
    def __init__(self, text, nxt=None):
        self.text = text
        self.incoming = list()
        self.connect(nxt)
    def connect(self, node):
        self.next = node
        if node and self not in node.incoming:
            node.incoming.append(self)
    def __repr__(self):
        return "%s(%s) to %s" % (self.__class__, self.text, str(self.next))

class StartNode(Node):
    def __init__(self, nxt=None):
        Node.__init__(self, "START", nxt)
        

class StopNode(Node):
    def __init__(self):
        Node.__init__(self, "STOP", None)
        
 
class InputNode(Node):
    def __init__(self, var, nxt=None):
        Node.__init__(self, "INPUT %s" % var, nxt)
        
        
class OutputNode(Node):
    def __init__(self, var, nxt=None):
        Node.__init__(self, " %s" % var, nxt)


class ConditionalNode(Node):
    def __init__(self, condition):
        Node.__init__(self, "%s?" % condition, None)
    def if_yes(self, node):
        self.yes = node
    def if_no(self, node):
        self.no = node
    def __repr__(self):
        return "%s(%s) no to %s" % (self.__class__, self.text, str(self.no))


class ConnectorNode(Node):
    def __init__(self):
        Node.__init__(self, "", None)
