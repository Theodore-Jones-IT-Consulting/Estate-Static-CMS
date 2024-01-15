def generate_content(params):
    name = params.get('name', 'World')
    return f"<p>Hello, {name}!</p>"
