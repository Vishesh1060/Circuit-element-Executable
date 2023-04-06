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
	    		o{{i}} : out std_ulogic
		{% endfor %}
	);
end {{entity_name}};

architecture {{entity_name}}_Arch of {{entity_name}} is
		{% for i in range(len(LRGates)) %}
			Signal var{{i}}:std_ulogic;
		{% endfor %}
	Begin
		{% for i in range(len(LRGates)) %}
			{% for j in range(len(LRGates[Gates[i]])-1) %}
				var{{i}}<= {{LRGates[Gates[i]][j]}} {{types[Gates[i]]['type']}} {{LRGates[Gates[i]][j+1]}};
			{% endfor %}
		{% endfor %}
end {{entity_name}}_Arch;