 entity e1 is
	port(
		i1: in std_ulogic;
		i2: in std_ulogic;
		i3: in std_ulogic;
		i4: in std_ulogic;
		o1: out std_ulogic
		);
end e1;

architecture e1_Arch of e1 is
		Signal var0:std_ulogic;	
		Signal var1:std_ulogic;
		Signal var2:std_ulogic;
	Begin
		var0<= i1 AND i2;
		var1<= i3 AND i4;
 		var2<= var0 OR var1;
		o1<=NOT var2
end e1_Arch;