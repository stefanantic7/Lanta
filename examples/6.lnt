use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;


dec $string_t: string = "string";
dec $int_t: string = "int";


dec $array: array = @array_init();
dec $broj: int = 0;
dec $running: int = 1;

loond($running == 1) {

	dec $unesite_broj_str: string = "Unesite broj:";
	dec $unet_broj_str: string = @cget($unesite_broj_str);
	dec $broj: int = @cast_to($unet_broj_str, $int_t);
	cond($broj < 0) {
		dec $running: int = 0;
	}
	cond($broj >= 0) {
		dec $koren: float = @sqrt($broj);
		cond(@is_integer($koren) == 1) {
			@array_append($array, $broj);
		}
	}
}
cond(@array_size($array) > 0) {
	dec $nula: int = 0;
	dec $array_element_1: int = @array_get($array, $nula);
	dec $output_string: string = @cast_to($array_element_1, $string_t);
	dec $index: int = 1;
	loond($index < @array_size($array)) {
		dec $array_element_index: int = @array_get($array, $index);
		dec $output_string: string = $output_string.", ".@cast_to($array_element_index, $string_t);
		dec $index: int = $index + 1;
	}

	dec $result: string = "Brojevi sa celim korenom: ".$output_string;
	@cput($result);
}