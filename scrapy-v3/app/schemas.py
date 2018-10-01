from marshmallow import fields, Schema

class CrawlSchema(Schema):
    _id = fields.Str(dump_only=True, description="Id of data")
    web = fields.Str(required=True, description="Url web crawl", example="https://example.com")
    data = fields.Str(description="data crawler", example="data")

    class Meta:
        fields = ('_id', 'web', 'data')
        # ordered = True

class ErrorSchema(Schema):
    message = fields.Str(required=True, description="The error message.",example="Something went wrong.")