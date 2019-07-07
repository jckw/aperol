from collections import OrderedDict
from functools import partial

import graphene
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene.types.argument import to_arguments
from graphene_django.filter.utils import (
    get_filtering_args_from_filterset,
    get_filterset_class,
)


class NonNullConnection(relay.Connection):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        super().__init_subclass_with_meta__(node=node, name=name, **options)

        # Override the original EdgeBase type to make to `node` field required.
        class EdgeBase:
            node = graphene.Field(
                cls._meta.node,
                description="The item at the end of the edge",
                required=True,
            )
            cursor = graphene.String(
                required=True, description="A cursor for use in pagination"
            )

        # Create the edge type using the new EdgeBase.
        edge_name = cls.Edge._meta.name
        edge_bases = (EdgeBase, graphene.ObjectType)
        edge = type(edge_name, edge_bases, {})
        cls.Edge = edge

        # Override the `edges` field to make it non-null list
        # of non-null edges.
        cls._meta.fields["edges"] = graphene.Field(
            graphene.NonNull(graphene.List(graphene.NonNull(cls.Edge)))
        )
