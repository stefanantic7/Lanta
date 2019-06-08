use cget, cput;
use cast_to;

dec $string_t: string = "string";
dec $int_t: string = "int";

dec $unesite_prvi: string = "Unesite prvi broj:";
dec $unesite_drugi: string = "Unesite drugi broj:";
dec $unesite_treci: string = "Unesite treci broj:";
dec $unesite_cetvrti: string = "Unesite cetvrti broj:";

dec $prvi_broj_str: string = @cget($unesite_prvi);
dec $drugi_broj_str: string = @cget($unesite_drugi);
dec $treci_broj_str: string = @cget($unesite_treci);
dec $cetvrti_broj_str: string = @cget($unesite_cetvrti);

dec $broj_1: int = @cast_to($prvi_broj_str, $int_t);
dec $broj_2: int = @cast_to($drugi_broj_str, $int_t);
dec $broj_3: int = @cast_to($treci_broj_str, $int_t);
dec $broj_4: int = @cast_to($cetvrti_broj_str, $int_t);
dec $max: int = 0;

cond( ($broj_1 > $broj_2) && ($broj_1 > $broj_3) && ($broj_1 > $broj_4) ) {
	dec $max: int = $broj_1;
}
cond( ($broj_2 > $broj_1) && ($broj_2 > $broj_3) && ($broj_2 > $broj_4) ) {
	dec $max: int = $broj_2;
}
cond( ($broj_3 > $broj_1) && ($broj_3 > $broj_2) && ($broj_3 > $broj_4) ) {
	dec $max: int = $broj_3;
}
cond( ($broj_4 > $broj_1) && ($broj_4 > $broj_2) && ($broj_4 > $broj_3) ) {
	dec $max: int = $broj_4;
}


dec $najveci_broj_je: string = "Najveci broj je:".@cast_to($max, $string_t);

@cput($najveci_broj_je);
