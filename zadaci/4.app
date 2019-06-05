use cget, cput;
use cast_to;

dec $zbir = 0;
dec $counter = 0;
dec $running = 1;

dec $broj: int = 0;
dec $avg: float = 0;

loond($running == 1) {
	$broj = @cast_to(@cget("Unesite broj:"), "int");
	cond($broj == 0) {
		$running = 0;
	}
	cond($broj != 0) {
		$counter = $counter +1 ;
		$zbir = $zbir + $broj;
	}
}
$avg = $zbir / $counter;
@cput("Aritmeticka sredina je:".@cast_to($avg, "string"));


