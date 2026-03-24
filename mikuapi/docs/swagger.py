# mikuapi/docs/swagger.py

def swagger_ui():
    return b"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MikuAPI Docs</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
    </head>
    <body>
        <div id="swagger-ui"></div>

        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>

        <script>
        const ui = SwaggerUIBundle({
            url: "/openapi.json",
            dom_id: "#swagger-ui",
        });
        </script>
    </body>
    </html>
    """