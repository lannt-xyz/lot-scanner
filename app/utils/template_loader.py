from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment to load templates from the "prompt_templates" directory
template_env = Environment(loader=FileSystemLoader("prompt_templates"))
