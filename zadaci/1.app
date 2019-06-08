use cget, cput;
use cast_to;
use str_equals;

dec $int_t: string = "int";
dec $string_t: string = "string";


dec $unesite_pol: string = "Unesite pol:"; 
dec $pol: string = @cget($unesite_pol);

dec $unesite_visinu: string = "Unesite Vasu visinu:";
dec $visina_str: string = @cget($unesite_visinu);

dec $visina: int = @cast_to($visina_str, $int);
dec $idealna_kilaza: int = 0;

dec $m: string = "m";

dec $f: string = "f";

cond(@str_equals($pol, $m) == 1) {
   dec $idealna_kilaza: int = $visina - 100;
}	
cond(@str_equals($pol, $f) == 1) {
   dec $idealna_kilaza: int = $visina - 120;
}

dec $result_str: string = "Vasa idealna kilaza je:".@cast_to($idealna_kilaza, string_t);
@cput($result_str);
