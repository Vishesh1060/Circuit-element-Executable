
Library ieee;
Use ieee.std_logic_1164.all;

entity entity is
	
	port (
		
	    		i0 : in std_ulogic;
		
	    		i1 : in std_ulogic;
		
		
	    		o1 : out std_ulogic
		
	    		o2 : out std_ulogic
		
	);
end entity;

architecture entity_Arch of entity is
		
			Signal var0:std_ulogic;
		
			Signal var1:std_ulogic;
		
			Signal var2:std_ulogic;
		
	Begin
		 var0  <= i0 xor i1
	 var1  <= var0 xor i1
	 var2  <= i0 xor var0
	
end entity_Arch;