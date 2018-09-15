import graphene
import aperol.properties.schema


class Query(aperol.properties.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
