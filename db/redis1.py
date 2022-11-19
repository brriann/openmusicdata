import redis
from redisgraph import Node, Edge, Graph, Path


# Demo Graph Structure

#                          -> Birds of Mind
# AcidPauli -> NicolasJaar
#                          -> Hot Since 82


r = redis.Redis(host='localhost', port=6379)
redis_graph = Graph('relatedArtists', r)


acidPauli = Node(label='artist', properties={'id': '3LHqODf1hGAgZ5LTw1Gf4C'})
redis_graph.add_node(acidPauli)

nicolasJaar = Node(label='artist', properties={'id': '5a0etAzO5V26gvlbmHzT9W'})
redis_graph.add_node(nicolasJaar)

birdsofMind = Node(label='artist', properties={'id': '6V4bkdqHvsJ2lqkIl4qnG7'})
redis_graph.add_node(birdsofMind)

hotSince82 = Node(label='artist', properties={'id': '1tRBmMtER4fGrzrt8O9VpS'})
redis_graph.add_node(hotSince82)


edge1 = Edge(acidPauli, 'relatedArtist', nicolasJaar, properties={'confidence': '0.95'})
redis_graph.add_edge(edge1)

edge2 = Edge(nicolasJaar, 'relatedArtist', birdsofMind, properties={'confidence': '0.97'})
redis_graph.add_edge(edge2)

edge3 = Edge(nicolasJaar, 'relatedArtist', hotSince82, properties={'confidence': '0.94'})
redis_graph.add_edge(edge3)

redis_graph.commit()

redis_graph.delete()