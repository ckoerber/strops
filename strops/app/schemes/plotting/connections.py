"""Plotting utilities for schmes modules."""
from typing import List, Dict, Any
from itertools import product

from networkx import all_simple_paths

from plotly.graph_objects import Figure, Parcoords
from plotly.offline import plot

from strops.app.schemes.models import ExpansionScheme
from strops.app.schemes.utils.graphs import get_connected_operators
from strops.app.operators.models import Operator
from strops.app.operators.templatetags.operators_extras import scale_name


def get_op_connections_data_plotly(
    schemes: List[ExpansionScheme],
) -> List[Dict[str, Any]]:
    """Prepares plotly parcoords data from schemes.

    Uses strops.app.schemes.utils.graphs.get_connected_operators to find connected
    operators.
    """
    scales = [scheme.source_scale for scheme in schemes] + [schemes[-1].target_scale]
    graph = get_connected_operators(schemes, prune=True)
    sources = Operator.objects.filter(
        id__in=schemes[0].relations.values_list("source__id", flat=True)
    )
    targets = Operator.objects.filter(
        id__in=schemes[-1].relations.values_list("target__id", flat=True)
    )

    paths = set()
    for source, target in product(sources, targets):
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
                ticktext=[str(op.expression).replace("*", "") for op in coords.keys()],
                tickvals=list(coords.values()),
            )
        )

    return data


def get_op_connections_graph_plotly(schemes: List[ExpansionScheme], **layout) -> str:
    """Creates plotly Parcoords grah (div without js) for schemes."""
    fig = Figure(
        data=Parcoords(dimensions=get_op_connections_data_plotly(schemes)),
        layout=layout,
    )
    return plot(fig, auto_open=False, output_type="div", include_plotlyjs=False)
