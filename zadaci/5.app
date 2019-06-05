use cget, cput;
use cast_to;
use random;

dec $n: int = @cast_to(@cget("Unesite broj:"), "int");
dec $broj: int = 0;
loond($n > 0) {
	$n = $n - 1;
	$broj = @random(1, 100);
	@cput("Random broj:".@cast_to($broj, "string"));
}

