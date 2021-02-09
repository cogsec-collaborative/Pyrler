#!/usr/bin/env python

# build a mention graph from a file of Parler posts data and write it
# out as a gexf file
#
#   ./network.py parler_posts.jsonl parler_posts.gexf
#
# to build the hashtag colocation graph (i.e. have the graph oriented around nodes that are hashtags
# instead of posts or users), use the --hashtags flag
#
#  ./network.py --hashtags parler_posts.jsonl parler_posts.gexf
#
# to build the echo graph, use the --echo flag
#
#  ./network.py --echo parler_posts.jsonl parler_posts.gexf
#
#

import sys
import json
import networkx
import optparse
import itertools
import time

from networkx import nx_pydot
from networkx.readwrite import json_graph

usage = "network.py parler_posts.jsonl graph.gexf"
opt_parser = optparse.OptionParser(usage=usage)

opt_parser.add_option(
    "--min_subgraph_size",
    dest="min_subgraph_size",
    type="int",
    help="remove any subgraphs with a size smaller than this number"
)

opt_parser.add_option(
    "--max_subgraph_size",
    dest="max_subgraph_size",
    type="int",
    help="remove any subgraphs with a size larger than this number"
)

opt_parser.add_option(
    "--hashtags",
    dest="hashtags",
    action="store_true",
    help="show hashtag relations instead of mention relations"
)

opt_parser.add_option(
    "--echo",
    dest="echo",
    action="store_true",
    help="show echo relations instead of mention relations"
)

options, args = opt_parser.parse_args()

if len(args) != 2:
    opt_parser.error("must supply input and output file names")

parler_posts, output = args

G = networkx.DiGraph()


def add(from_user, from_id, to_user, to_id, type, created_at=None):
    # Adds a relation to the graph
    # Note: storing start_data will allow for timestamps for gephi timeline, where nodes will appear on screen at their start dataset
    # and stay on forever after

	G.add_node(from_user, screen_name=from_user, start_date=created_at)
	G.add_node(to_user, screen_name=to_user, start_date=created_at)

	if G.has_edge(from_user, to_user):
		weight = G[from_user][to_user]['weight'] + 1
	else:
		weight = 1
	G.add_edge(from_user, to_user, type=type, weight=weight)

def convert_date(unconverted_date):
    # Converts 14 digit time to 'dd/MM/yyyy HH:mm:ss' format
    # and returns newly formatted date
    unconverted_date = str(unconverted_date)
    converted_date = time.strftime('%d/%m/%Y %H:%M:%S', time.strptime(unconverted_date,'%Y%m%d%H%M%S'))
    return converted_date

for line in open(parler_posts):
    try:
        t = json.loads(line)
    except:
        continue
    from_id = t['_id']
    from_user = t['creator']['username']
    from_user_id = t['creator']['id']
    to_user = None
    to_id = None
    created_at_date = convert_date(t["createdAt"])

    if options.hashtags: # hashtag graph
        hashtags = t['hashtags']
        hashtag_pairs = list(itertools.combinations(hashtags, 2)) # list of all possible hashtag pairs
        for u in hashtag_pairs:
            # source hashtag: u[0]
            # target hashtag: u[1]
            add('#' + u[0], None, '#' + u[1], None, 'hashtag', created_at_date)
    elif options.echo: # echo graph
        if "parent" in t:
            # t['parent']['creator'] is ID of creator whereas t['parent']['_id'] is ID of the post
            # t['parent'] does not include parent username
            add(from_user, from_id, t['parent']['creator'], t['parent']['_id'], 'echo', created_at_date)
    else: # mention graph
        for (screen_name, user_id) in t['@'].items():
            add(from_user, from_id, screen_name, user_id, 'mention', created_at_date)


if options.min_subgraph_size or options.max_subgraph_size:
    g_copy = G.copy()
    for g in networkx.connected_component_subgraphs(G):
        if options.min_subgraph_size and len(g) < options.min_subgraph_size:
            g_copy.remove_nodes_from(g.nodes())
        elif options.max_subgraph_size and len(g) > options.max_subgraph_size:
            g_copy.remove_nodes_from(g.nodes())
    G = g_copy

networkx.write_gexf(G, output)
