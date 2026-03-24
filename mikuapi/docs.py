# mikuapi/docs.py

def generate_docs(routes):
    html = """
    <html>
    <head>
        <title>MikuAPI Docs</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #333; }
            .route { margin-bottom: 10px; }
            .method { font-weight: bold; color: green; }
        </style>
    </head>
    <body>
        <h1>🚀 MikuAPI Documentation</h1>
    """

    for route in routes:
        html += f"""
        <div class="route">
            <span class="method">{route.method}</span>
            <span>{route.path}</span>
        </div>
        """

    html += "</body></html>"
    return html.encode()