#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import json
import pdb

def add_character(graph, name, appeared=True):
    if not graph.has_node(name):
        graph.add_node(name, appeared=appeared)

if __name__ == "__main__":
    with open('data.json', encoding="utf-8") as f:
        data = json.load(f)

    G = nx.DiGraph()
    for entry in data:
        char_from = entry['from'].strip()
        char_to = entry['to'].strip()
        label = entry['label'].strip()

        episode = entry['episode'] if 'episode' in entry else ''
        timestamp_begin = entry['timestamp']['begin'] if 'timestamp' in entry else ''
        timestamp_end = entry['timestamp']['end'] if 'timestamp' in entry else ''

        if entry['type'] == 'battle':
            G.add_node(char_from, appeared=True)
            G.add_node(char_to, appeared=True)
            G.add_edge(char_from, char_to, label=label, kind="battle", episode=episode, timestamp_begin=timestamp_begin, timestamp_end=timestamp_end)
            G.add_edge(char_to, char_from, label="", kind="battle", episode=episode, timestamp_begin=timestamp_begin, timestamp_end=timestamp_end)
        elif entry['type'] in ['mention', 'cameo']:
            G.add_node(char_from, appeared=True)

            is_callback, is_foreshadow = False, False
            mentioned_person_has_appeared = G.has_node(char_to)
            mentioned_person_will_appear = len([x for x in data if (((x['from'] == char_to) or (x['to'] == char_to)) and x['type'] == "battle")]) > 0

            if mentioned_person_has_appeared:
                is_callback = True
            else:
                if mentioned_person_will_appear:
                    G.add_node(char_to, appeared=True)
                    is_foreshadow = True
                else:
                    G.add_node(char_to, appeared=False)

            if entry['type'] == 'cameo':
                G.add_edge(char_from, char_to, label=("cameo" if label == "" else label), kind="cameo", callback=is_callback, foreshadow=is_foreshadow, implicit=False, episode=episode, timestamp_begin=timestamp_begin, timestamp_end=timestamp_end)
                G.add_edge(char_to, char_from, label="", kind="cameo", episode=episode, timestamp_begin=timestamp_begin, timestamp_end=timestamp_end)

            if entry['type'] == 'mention':
                is_implicit = False
                if 'implicit' in entry and entry['implicit'] is True:
                    is_implicit = True

                G.add_edge(char_from, char_to, label=label, kind="mention", callback=is_callback, foreshadow=is_foreshadow, implicit=is_implicit, episode=episode, timestamp_begin=timestamp_begin, timestamp_end=timestamp_end)

    filename = "network"
    with open(filename + ".json", "w+", encoding="utf8") as f:
        D = G.copy()
        #D.remove_nodes_from([x for x, y in D.nodes(data=True) if not y['appeared']])
        json.dump(nx.cytoscape_data(D), f, indent=4)
    nx.write_gml(G, filename + ".gml")
