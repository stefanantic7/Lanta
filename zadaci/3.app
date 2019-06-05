use cget, cput;
use cast_to;

dec $broj_1: int = @cast_to(@cget("Unesite prvi broj:"), "int");
dec $broj_2: int = @cast_to(@cget("Unesite drugi broj:"), "int");
dec $broj_3: int = @cast_to(@cget("Unesite treci broj:"), "int");
dec $broj_4: int = @cast_to(@cget("Unesite cetvrti broj:"), "int");
dec $max: int = 0;

cond($broj_1 > $broj_2 && $broj_1 > $broj_3 && $broj_1 > $broj_4) {
   $max = $broj_1;
}
cond($broj_2 > $broj_1 && $broj_2 > $broj_3 && $broj_2 > $broj_4) {
   $max = $broj_2;
}
cond($broj_3 > $broj_1 && $broj_3 > $broj_2 && $broj_3 > $broj_4) {
   $max = $broj_3;
}
cond($broj_4 > $broj_1 && $broj_4 > $broj_2 && $broj_4 > $broj_3) {
   $max = $broj_4;
}

@cput("Najveci broj je:".@cast_to($max, "string"));
