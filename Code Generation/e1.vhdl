
Library ieee;
Use ieee.std_logic_1164.all;

entity entity is
	
	port (
		
	    		i0 : in std_ulogic;
		
	    		i1 : in std_ulogic;
		
	    		i2 : in std_ulogic;
		
	    		i3 : in std_ulogic;
		
		
	    		o1 : out std_ulogic
		
	);
end entity;

architecture entity_Arch of entity is
		
			Signal var0:std_ulogic;
		
			Signal var1:std_ulogic;
		
			Signal var2:std_ulogic;
		
			Signal var3:std_ulogic;
		
	Begin
		
		var0 <= i1 AND i2
		var1 <= i3 AND i4
		var2 <= var0 OR var1
		o1 <= NOT var2
end entity_Arch;