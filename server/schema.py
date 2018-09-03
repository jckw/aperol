import graphene
import server.properties.schema


class Query(server.properties.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
