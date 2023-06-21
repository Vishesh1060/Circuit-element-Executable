
Library ieee;
Use ieee.std_logic_1164.all;

entity entity is
	
	port (
		
	    		i0 : in std_ulogic;
		
	    		i1 : in std_ulogic;
		
	    		i2 : in std_ulogic;
		
	    		i3 : in std_ulogic;
		
		
	    		o1 : out std_ulogic
		
	    		o2 : out std_ulogic
		
	    		o3 : out std_ulogic
		
	    		o4 : out std_ulogic
		
	);
end entity;

architecture entity_Arch of entity is
		
			Signal var0:std_ulogic;
		
			Signal var1:std_ulogic;
		
			Signal var2:std_ulogic;
		
			Signal var3:std_ulogic;
		
	Begin
		 var0  <= i2 or i3
	 var1  <= not i0
	 var2  <= var1 or i1
	 var3  <= var2 and var0
	 o0  <=  var3
	
end entity_Arch;