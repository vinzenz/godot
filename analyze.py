import json
from jinja2 import Template

data = None
with open('premake.json', 'r') as f:
    data = json.loads(f.read())

ProjectTmpl = Template("""
solution "godot"
    configurations {"debug"}
{% for data in alldata.values() %}
{% if data['type'] == 'Library'%}
    project "{{data['name']}}.{{data['platform']}}"
        kind "StaticLib"{% else %}
    project "{{data['name'].split('/')[-1]}}"
        kind "ConsoleApp"{%endif %}
        language "C++"
        files { {% for file in data['sources'] %}
                        "{{file}}",{% endfor%}
                    }
        includedirs { {% for dir in data['includedirs'] %}
                        "{{dir}}",{% endfor%}
                    }
        defines { {% for define in data['defines'] %}
                        "{{define}}",{% endfor%}
                    }
        {% if data['libs'] %}
        links {
        {% for lib in data['libs'] %}{% if '$' in lib %}"{{lib.replace('$', '')}}",{% elif '.srv' in lib %}"{{lib.replace('srv', 'server')}}",{% else %}"{{lib}}.{{data["platform"]}}",{% endif %}{% endfor %}
              }
        {% endif %}
	buildoptions {
		{% for item in data.get('ccflags', []) %}
		"{{item}}",{% endfor %}
	}
{% endfor %}
""")

print ProjectTmpl.render(alldata=data).replace('\\', '\\\\')
