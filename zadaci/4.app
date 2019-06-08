use cget, cput;
use cast_to;

dec $string_t: string = "string";
dec $int_t: string = "int";

dec $zbir: int = 0;
dec $counter: int = 0;
dec $running: int = 1;

dec $broj: int = 0;
dec $avg: float = 0;



loond($running == 1) {
	dec $unesite_broj_str: string = "Unesite broj:";
	dec $unet_broj_str: string = @cget($unesite_broj_str);

	dec $broj: int = @cast_to($unet_broj_str, $int_t);
	
	cond($broj == 0) {
		dec $running: int = 0;
	}
	cond($broj != 0) {
		dec $counter: int = $counter +1 ;
		dec $zbir: int = $zbir + $broj;
	}
}
dec $avg: float = $zbir / $counter;
dec $result_str: string = "Aritmeticka sredina je: ".@cast_to($avg, $string_t);
@cput($result_str);


