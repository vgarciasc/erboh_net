import networkx as nx
import json
import pdb

def add_character(graph, name, appeared=True):
    if not graph.has_node(name):
        graph.add_node(name, appeared=appeared)

if __name__ == "__main__":
    with open('data.json') as f:
        data = json.load(f)

        G = nx.Graph()
        for entry in data:
            if entry['type'] == 'battle':
                add_character(G, entry['from'], appeared=True)
                add_character(G, entry['to'], appeared=True)
                G.add_edge(entry['from'], entry['to'], label=entry['label'], foreshadow=False)
                G.add_edge(entry['to'], entry['from'], label=entry['label'], foreshadow=False)
            elif entry['type'] in ['mention', 'mention-bg']:
                add_character(G, entry['from'], appeared=True)
                add_character(G, entry['to'], appeared=True)
                G.add_edge(entry['from'], entry['to'], label=entry['label'], foreshadow=False)
            elif entry['type'] == 'mention-doesnt-exist':
                add_character(G, entry['from'], appeared=True)
                add_character(G, entry['to'], appeared=False)
                G.add_edge(entry['from'], entry['to'], label=entry['label'], foreshadow=False)
            elif entry['type'] == 'mention-didnt-exist':
                add_character(G, entry['from'], appeared=True)
                add_character(G, entry['to'], appeared=True)
                G.add_edge(entry['from'], entry['to'], label=entry['label'], foreshadow=True)
            else:
                print("ERROR:", entry['type'])

        nx.write_gml(G, "network_s5.gml")
