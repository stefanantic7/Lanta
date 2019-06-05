use cget, cput;
use cast_to;

dec $pol: string = @cget("Unesite pol:");
dec $visina: int = @cast_to(@cget("Unesite Vasu visinu:"), "int");
dec $idealna_kilaza: int = 0;

cond($pol == "m") {
   $idealna_kilaza = $visina - 100;
}
cond($pol == "f") {
   $idealna_kilaza = $visina - 120;
}

@cput("Vasa idealna kilaza je:".@cast_to($idealna_kilaza, "string"));
