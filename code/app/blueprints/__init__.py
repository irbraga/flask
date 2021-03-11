'''
Module with common configuration for the Blueprints.
'''

# https://swagger.io/docs/specification/2-0/authentication/
__auth_types = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key"
    }
}
