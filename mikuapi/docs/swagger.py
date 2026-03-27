def swagger_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MikuAPI Docs</title>

        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">

        <style>
            body {
                margin: 0;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: #f5f5f7;
                color: #111;
            }

            .container {
                max-width: 900px;
                margin: auto;
                padding: 16px;
            }

            .header {
                background: white;
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            }

            .title {
                font-size: 22px;
                font-weight: 600;
            }

            .subtitle {
                font-size: 14px;
                color: #666;
            }

            .swagger-ui .topbar {
                display: none;
            }

            .swagger-ui .opblock {
                border-radius: 10px !important;
                margin-bottom: 10px;
            }
        </style>
    </head>

    <body>

        <div class="container">
            <div class="header">
                <div class="title">MikuAPI</div>
                <div class="subtitle">Lightweight Python Framework</div>
            </div>

            <div id="swagger-ui"></div>
        </div>

        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>

        <script>
        SwaggerUIBundle({
            url: "/openapi.json",
            dom_id: "#swagger-ui",
            deepLinking: true,
            docExpansion: "none",
            defaultModelsExpandDepth: -1
        });
        </script>

    </body>
    </html>
    """.encode()