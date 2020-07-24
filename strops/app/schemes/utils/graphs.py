"""Tools related to identifying connections between different scales."""
from typing import List, Tuple, Any, Optional, Dict, Union

from strops.app.operators.models import Operator
from strops.app.schemes.models import ExpansionScheme
from networkx import MultiDiGraph, all_simple_paths, bfs_tree


def construct_multi_di_graph(edges: List[Tuple[str, str, Any]]) -> MultiDiGraph:
    """Constructs a multi directed graph from a list of edges.

    Arguments:
        edges: A list of tuples with entries: start, end and identifier.
    """
    g = MultiDiGraph()
    for start, end, key in edges:
        g.add_edge(start, end, key=key)
    return g


def construct_scale_graph(instance_as_key: bool = False) -> MultiDiGraph:
    """A multi directed graph for all expansion schemes.

    The identifier for different edges is the primary key of the expansion scheme.

    Arguments:
        instance_as_key: If True, edge-keys will be scheme instances instead of scheme
        ids.
    """
    if not instance_as_key:
        edges = ExpansionScheme.objects.values_list(
            "source_scale", "target_scale", "pk"
        )
    else:
        edges = []
        for scheme in ExpansionScheme.objects.all():
            edges.append((scheme.source_scale, scheme.target_scale, scheme))
    return construct_multi_di_graph(edges)


def get_scales_with_connections(graph: Optional[MultiDiGraph] = None):
    """Return list of scales which have at least one connection.

    Arguments:
        graph: The graph to look up. Defaults to ExpansionScheme graph.
    """
    graph = graph or construct_scale_graph()
    return list(node for node in graph if graph.neighbors(node))


def get_connected_scales(scale: str, graph: Optional[MultiDiGraph] = None):
    """Return list of connected scales for given scale.

    Arguments:
        scale: The scale to start.
        graph: The graph to look up. Defaults to ExpansionScheme graph.
    """
    graph = graph or construct_scale_graph()
    return (
        list(node for node in bfs_tree(graph, scale).nodes if node != scale)
        if scale in graph
        else list()
    )


def get_scale_branches(
    source_scale: str,
    target_scale: str,
    graph: Optional[MultiDiGraph] = None,
    instance_as_key: bool = False,
) -> Dict[List[str], List[Tuple[str, str, Union[int, ExpansionScheme]]]]:
    """Returns possible branches for starting from source and going to target.

    The keys of the dictionary correspond to the scales of an entire path, values are
    lists specifying choices at each step. This step tuple has the entries, start scale
    of step, end scale of step and a set of different expansion schemes at this step.

    Arguments:
        source_scale: The scale to start.
        target_scale: The scale to end.
        graph: The graph to look up. Defaults to ExpansionScheme graph.
        instance_as_key: If true, returned schemes are ExpansionScheme instances
            instead of ids.
    """
    graph = graph or construct_scale_graph(instance_as_key=instance_as_key)
    unique_scale_paths = set(
        map(tuple, all_simple_paths(graph, source=source_scale, target=target_scale))
    )

    multi_paths = dict()
    for path in unique_scale_paths:
        scale_bridges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        steps = []
        for start_scale, target_scale in scale_bridges:
            scheme_choices = set(graph[start_scale][target_scale].keys())
            steps.append((start_scale, target_scale, scheme_choices))

        multi_paths[path] = steps

    return multi_paths


def get_connected_operators(
    schemes: List[ExpansionScheme], prune: bool = True
) -> MultiDiGraph:
    """
    """
    graph = MultiDiGraph()
    for scheme in schemes:
        for relation in scheme.relations.all():
            graph.add_edge(relation.source, relation.target, key=relation)

    if prune:
        source_ops = Operator.objects.filter(
            id__in=schemes[0].relations.values_list("source__id", flat=True)
        )
        target_ops = Operator.objects.filter(
            id__in=schemes[-1].relations.values_list("target__id", flat=True)
        )

        connected_to_source = set()
        for node in source_ops:
            # This includes source ops (start nodes)
            connected_to_source |= set(bfs_tree(graph, node).nodes)

        connected_to_target = set()
        for node in target_ops:
            # This includes target ops (start nodes)
            connected_to_target |= set(bfs_tree(graph, node, reverse=True).nodes)

        unconnected = set(graph.nodes) - (connected_to_source & connected_to_target)
        graph.remove_nodes_from(unconnected)

    return graph
