use cget, cput;
use cast_to;

dec $broj: int = @cast_to(@cget("Unesite broj:"), "int");
dec $zbir_cifara: int = 0;

loond($broj != 0) {
    $zbir_cifara = $zbir_cifara + ($broj % 10);
    $broj = $broj // 10;
}

@cput("Zbir cifara unetog broja je:".@cast_to($zbir_cifara, "string"));

cond($zbir_cifara > 10) {
	@cput("Zbir cifara unetog broja je veci od 10"));
}

cond($zbir_cifara < 10) {
	@cput("Zbir cifara unetog broja je manji od 10"));
}
