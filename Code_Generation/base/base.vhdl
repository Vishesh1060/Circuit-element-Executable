{# Base Layout  #}
Library ieee;
Use ieee.std_logic_1164.all;

entity {{entity_name}} is
	{% if generic_present is true %}
		generic (
   		{{generic_name}} : {{generic_type}} := {{generic_value}};
		);
	{% endif %}
	port (
		{% for i in range(Terminals["in"]) %}
	    		i{{i}} : in std_ulogic;
		{% endfor %}
		{% for i in range(Terminals["out"]) %}
	    		o{{i+1}} : out std_ulogic
		{% endfor %}
	);
end {{entity_name}};

architecture {{entity_name}}_Arch of {{entity_name}} is
		{% for i in range(LRGates|length) %}
			Signal var{{i}}:std_ulogic;
		{% endfor %}
	Begin
		{{core_out}}
end {{entity_name}}_Arch;