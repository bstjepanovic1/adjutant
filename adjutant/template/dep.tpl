{% for filename, deps in data.items() %}
{{filename}}: \\
	{% for dep in deps %}
	{{dep}} \\
	{% endfor %}
	
{% endfor %}
