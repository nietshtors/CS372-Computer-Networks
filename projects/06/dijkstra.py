import sys
import json
import math  # If you want to use math.inf for infinity


class Graph:
    def __init__(self, routers: dict):
        self.routers = routers
        self.nodes = [r for r in routers.keys()]
        for r in self.nodes:
            for x in routers[r]['connections'].keys():
                if x not in self.nodes: self.nodes.append(x)
        self.adjmat = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
        self.setup()
        
    def __str__(self):
        s = ''
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                s += f'{self.adjmat[i][j]:4d}'
            s += '\n'
        return s

    def setup(self):
        for r in self.nodes:
            row = self.get_index(r)
            connections = self.routers[r]['connections']
            for c in connections.keys():
                column = self.get_index(c)
                weight = connections[c]['ad']
                self.adjmat[row][column] = weight
                
    def get_index(self, ip):
        return self.nodes.index(ip)
    
    def dist(self, src, dest):
        return self.adjmat[self.get_index(src)][self.get_index(dest)]
    
    def neighbors(self, src, queue):
        return [n for n in self.nodes if self.adjmat[self.get_index(src)][self.get_index(n)] != 0 and n in queue]
                

def ipv4_to_value(ipv4_addr) -> int:
    """
    Convert a dots-and-numbers IP address to a single 32-bit numeric
    value of integer type. Returns an integer type.
    """

    arr = ipv4_addr.split('.')
    arr.reverse()
    val = 0
    for i in range(4):
        val |= int(arr[i]) << 8 * i
    return val


def get_subnet_mask_value(slash) -> int:
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number of integer type. The input can contain an IP
    address optionally, but that part should be discarded.
    """

    num = int(slash.split('/')[1])
    return 0xffffffff & ~((1 << (32-num))-1)


def ips_same_subnet(ip1: str, ip2: str, slash: str) -> bool:
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.
    """

    ip1 = ipv4_to_value(ip1)
    ip2 = ipv4_to_value(ip2)
    subnet_mask = get_subnet_mask_value(slash)
    return ip1 & subnet_mask == ip2 & subnet_mask


def find_router_for_ip(routers: str, ip: str):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.
    """

    for router, d in routers.items():
        if ips_same_subnet(ip, router, d['netmask']): return router
    return None


def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    def min_(to_visit, dist):
        distance = math.inf
        node = ''
        for n in to_visit:
            if dist[n] <= distance:
                node = n
                distance = dist[n]
        return node
    
    src_r = find_router_for_ip(routers, src_ip)
    dest_r = find_router_for_ip(routers, dest_ip)    
    if src_r == dest_r: return []
    
    graph = Graph(routers)
    dist = {n: math.inf for n in graph.nodes}
    parent = {n: None for n in graph.nodes}
    dist[src_r] = 0
    

    to_visit = graph.nodes.copy()
    while to_visit:
        current = min_(to_visit, dist)
        to_visit.remove(current)

        for neighbor in graph.neighbors(current, to_visit):
            alt = dist[current] + graph.dist(current, neighbor)
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                parent[neighbor] = current

    current = dest_r
    path = []
    while current != src_r:
        path.append(current)
        current = parent[current]
    path.append(src_r)
    path.reverse()
    
    return path
        

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

