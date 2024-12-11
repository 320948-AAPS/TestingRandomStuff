#tinyAI.py
import random

class Node:
    def __init__(self, id):
        self.id = id
        self.links = list()
        self.weight = 0.01

class Link:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.weight = 0.01

class Network:
    def __init__(self):
        self.input_layer = list()
        self.hidden_layer = list()
        self.output_layer = list()

    def reset_weights(self, nodes):
        for node in nodes:
            node.weight = 0.0
            for link in node.links:
                link.weight = 0.0

    def reset(self):
        self.reset_weights(self.input_layer)
        self.reset_weights(self.hidden_layer)
        self.reset_weights(self.output_layer)

def normalize(nodes):
    max_weight = max(node.weight for node in nodes)
    if max_weight == 0:
        return
    for node in nodes:
        node.weight /= max_weight

def run_network(network, input_data, answer):
    for i in range(4):
        network.input_layer[i].weight = input_data[i]
    for node in network.input_layer:
        for link in node.links:
            link.end.weight += node.weight * link.weight

    normalize(network.hidden_layer)

    for node in network.hidden_layer:
        for link in node.links:
            link.end.weight += node.weight * link.weight
        
    normalize(network.output_layer)

    horizontal_weight = network.output_layer[0].weight
    vertical_weight = network.output_layer[1].weight

    if answer == "horizontal":
        if horizontal_weight - vertical_weight > 0.01:
            return 1.0
        else:
            return 0.0
    if vertical_weight - horizontal_weight > 0.01:
        return 1.0
    else:
        return 0.0

# build network
nodes = []
for i in range(9):
    node = Node(i)
    nodes.append(node)

n0 = nodes[0]
n1 = nodes[1]
n2 = nodes[2]
n3 = nodes[3]
n4 = nodes [4]
n5 = nodes[5]
n6 = nodes [6]
n7 = nodes[7]
n8 = nodes [8]

n0.links.append(Link(n0, n4))
n0.links.append(Link(n0, n5))
n0.links.append(Link(n0, n6))
n1.links.append(Link(n1, n4))
n1.links.append(Link(n1, n5))
n1.links.append(Link(n1, n6))
n2.links.append(Link(n2, n4))
n2.links.append(Link(n2, n5))
n2.links.append(Link(n2, n6))
n3.links.append(Link(n3, n4))
n3.links.append(Link(n3, n5))
n3.links.append(Link(n3, n6))
n4.links.append(Link(n4, n7))
n4.links.append(Link(n4, n8))
n5.links.append(Link(n5, n7))
n5.links.append(Link(n5, n8))
n6.links.append(Link(n6, n7))
n6.links.append(Link(n6, n8))

network = Network()
network.input_layer.append(n0)
network.input_layer.append(n1)
network.input_layer.append(n2)
network.input_layer.append(n3)

network.hidden_layer.append(n4)
network.hidden_layer.append(n5)
network.hidden_layer.append(n6)

network.output_layer.append(n7)
network.output_layer. append(n8)

data = [
    [ 1, 1,
      0, 0,], # horizontal

    [ 0, 0,
      1, 1,], # horizontal

    [ 1, 0,
      1, 0,], # vertical

    [ 0, 1,
      0, 1,], # vertical
    ]

links = []
for node in nodes:
    links.extend(node.links)

solution = []
best_score = 0
#training
while best_score < 8:
    network.reset()
    #randomly assign weights to links
    for link in links:
        link.weight = random.random()
    
    # check network functions
    score = 0
    score += run_network(network, data[0], "horizontal")
    score += run_network(network, data[1], "horizontal")
    score += run_network(network, data[2], "vertical")
    score += run_network(network, data[3], "vertical")
    # run again with a scrambled order
    score += run_network(network, data[1], "horizontal")
    score += run_network(network, data[0], "horizontal")
    score += run_network(network, data[3], "vertical")
    score += run_network(network, data[2], "vertical")

    if best_score < score:
        best_score = score
        solution.clear()
        for link in links:
            solution.append((link, link.weight))
    
    print(best_score)

for sol in solution:
    link = sol[0]
    weight = sol[1]
    # print the two nodes each link connects and its end weight
    print(f'{link.start.id},{link.end.id},{weight:0.2f},')

while True:
    user_input = input("upper-left upper-right lower-left lower-right ")
    type = input("Horizontal or vertical? ")
    input_mapped = map(int, user_input.split())
    data_to_use = []

    for i in input_mapped:
        data_to_use.append(i)
    
    if run_network(network, data_to_use, type) == 1.0:
        print("AI got it correct!")
    else:
        print("AI is wrong!")