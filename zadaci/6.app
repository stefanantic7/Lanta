use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;

dec $array: array = @array_init();
dec $broj: int = 0;
dec $running: int = 1;

loond($running == 1) {
	$broj = @cast_to(@cget("Unesite broj:"), "int");
	cond($broj < 0) {
		$running = 0;
	}
	cond($broj >= 0) {
		cond(@is_integer(@sqrt($broj))) {
			@array_append($array, $broj);
		}
	}
}
cond(@array_size($array) > 0) {
	dec $output_string: string = @cast_to(@array_get($array, 0), "string");
	dec $index: int = 1;
	loond($index < @array_size($array)) {
		$output_string = $output_string.", ".@cast_to(@array_get($array, $index), "string");
		$index = $index + 1;
	}
	@cput("Brojevi sa celim korenom: ".$output_string);
}