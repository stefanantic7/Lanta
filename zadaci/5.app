use cget, cput;
use cast_to;
use random;

dec $string_t: string = "string";
dec $int_t: string = "int";


dec $unesite_broj_str: string = "Unesite broj:";
dec $unet_broj_str: string = @cget($unesite_broj_str);

dec $n: int = @cast_to($unet_broj_str, $int_t);
dec $broj: int = 0;
loond($n > 0) {
	dec $n: int = $n - 1;
	dec $from: int = 1;
	dec $to: int = 100;
	dec $broj: int = @random($from, $to);

	dec $random_broj_str: string = "Random broj:".@cast_to($broj, $string_t);
	@cput($random_broj_str);
}

