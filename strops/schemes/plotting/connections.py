"""Plotting utilities for schmes modules."""
from typing import List, Dict, Any
from itertools import product

from networkx import all_simple_paths, MultiDiGraph

from plotly.graph_objects import Figure, Parcoords
from plotly.offline import plot

from strops.schemes.models import ExpansionScheme
from strops.schemes.plotting.tex_subs import sympy_subs
from strops.operators.models import Operator
from strops.operators.templatetags.operators_extras import scale_name


def get_op_connections_data_plotly(
    schemes: List[ExpansionScheme], graph: MultiDiGraph
) -> List[Dict[str, Any]]:
    """Prepares plotly parcoords data from schemes.

    Uses strops.schemes.utils.graphs.get_connected_operators to find connected
    operators.
    """
    scales = [scheme.source_scale for scheme in schemes] + [schemes[-1].target_scale]
    sources = Operator.objects.filter(source_for__scheme=schemes[0]).distinct()
    targets = Operator.objects.filter(target_of__scheme=schemes[-1]).distinct()

    paths = set()
    for source, target in product(sources, targets):
        if source in graph.nodes and target in graph.nodes:
            paths |= set(map(tuple, all_simple_paths(graph, source, target)))

    data = []
    for n_scale, scale in enumerate(scales):
        ops = Operator.objects.filter(scale=scale)
        coords = {op: num / (len(ops) - 1) for num, op in enumerate(ops)}
        data.append(
            dict(
                range=[0, 1],
                label=scale_name(scale),
                values=[coords[op] for op in [path[n_scale] for path in paths]],
                ticktext=[sympy_subs(op.expression) for op in coords.keys()],
                tickvals=list(coords.values()),
            )
        )

    return data


def get_op_connections_graph_plotly(
    schemes: List[ExpansionScheme], graph: MultiDiGraph, **layout
) -> str:
    """Creates plotly Parcoords grah (div without js) for schemes."""
    fig = Figure(
        data=Parcoords(dimensions=get_op_connections_data_plotly(schemes, graph)),
        layout=layout,
    )
    return plot(fig, auto_open=False, output_type="div", include_plotlyjs=False)
