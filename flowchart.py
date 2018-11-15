from node import *
from regexes import *
from sys import argv
import pickle

if len(argv) < 3:
    print("Usage: python3 %s [input code file] [output flowchart file]" % argv[0])
    raise SystemExit()


"""
start = StartNode()
a_in = InputNode("A")
b_in = InputNode("B")
a_lt_b = ConditionalNode("A < B")
a_dec_b = Node("A = A - B")
a_out = OutputNode("A")
stop = StopNode()

start.connect(a_in)
a_in.connect(b_in)
b_in.connect(a_lt_b)
a_lt_b.if_yes(a_out)
a_lt_b.if_no(a_dec_b)
a_dec_b.connect(a_lt_b)
a_out.connect(stop)

walkthrough(start)
"""


lines = list(filter(lambda c: len(c), map(lambda line: line.rstrip().replace("    ", "~"), open(argv[1]))))


def get_handle(code):
    nodes = list()
    while len(code):
        line = code[0]
        print(line)
        if line[-1] == ":":
            blank = ConnectorNode()
            print("block node")
            if loop.match(line):
                print("loop node")
                loop_br = ConditionalNode(loop.match(line).groups()[0])
                body = list()
                while (len(code)-1) and code[1][0] == "~":
                    body.append(code[1][1:])
                    del code[1]
                print("body: %s" % str(body))
                body_flow = get_handle(body)
                print("body flow: %s" % str(body_flow))
                
                loop_br.if_yes(body_flow[0])
                body_flow[-1].connect(loop_br)
                loop_br.if_no(blank)
                if len(nodes):
                    nodes[-1].connect(loop_br)
                else:
                    nodes.append(loop_br)
            elif branch.match(line):
                print("conditional node")
                con_br = ConditionalNode(branch.match(line).groups()[0])
                body = list()
                while (len(code)-1) and code[1][0] == "~":
                    body.append(code[1][1:])
                    del code[1]
                print("body: %s"% str(body))
                body_flow = get_handle(body)
                print("body flow: %s" % str(body_flow))
                if len(code)-1 and code[1] == "else:":
                    print("ELSE CLAUSE PRESENT")
                    else_body = list()
                    print(code)
                    del code[1]
                    while (len(code)-1) and code[1][0] == "~":
                        print(code)
                        else_body.append(code[1][1:])
                        del code[1]
                    print("else body: %s" % str(else_body))
                    else_body_flow = get_handle(else_body)
                    print("else body flow: %s" % str(else_body_flow))
                    con_br.if_yes(body_flow[0])
                    con_br.if_no(else_body_flow[0])
                    body_flow[-1].connect(blank)
                    else_body_flow[-1].connect(blank)
                else:
                    con_br.if_yes(body_flow[0])
                    body_flow[-1].connect(blank)
                    con_br.if_no(blank)
                print(nodes)
                if len(nodes):
                    nodes[-1].connect(con_br)
                else:
                    nodes.append(con_br)

            nodes.append(blank)
              
        elif read.match(line):
            this = InputNode(read.match(line).groups()[0])
            if len(nodes):
                nodes[-1].connect(this)
            nodes.append(this)
        elif write.match(line):
            this = OutputNode(write.match(line).groups()[0])
            if len(nodes):
                nodes[-1].connect(this)
            nodes.append(this)
        else:
            this = Node(line)
            if len(nodes):
                nodes[-1].connect(this)
            nodes.append(this)
        del code[0]
        print(nodes)
    return nodes
        
process = get_handle(lines)
begin = StartNode()
begin.connect(process[0])
end = StopNode()
process[-1].connect(end)

pickle.dump(begin, open(argv[2], "wb"))
