entity e1 is
	port(
		i1: in std_ulogic_vector(3 downto 0);
		o1: out std_ulogic
		);
end e1;

architecture e1_Arch of e1 is
		Signal var0:std_ulogic;	
		Signal var1:std_ulogic;
		Signal var2:std_ulogic;
	Begin
		var0<= i1(0) AND i1(1);
		var1<= i1(2) AND i1(3);
 		var2<= var0 OR var1;
		o1<=NOT var2
end e1_Arch;