use cget, cput;
use cast_to;

dec $string_t: string = "string";
dec $int_t: string = "int";

dec $unesite_broj: string = "Unesite broj:";
dec $unet_broj: int = @cget($unesite_broj);
dec $broj: int = @cast_to($unet_broj, $int_t);
dec $zbir_cifara: int = 0;

loond($broj != 0) {
	dec $zbir_cifara: int = $zbir_cifara + ($broj % 10);
	dec $broj: int = $broj // 10;
}

dec $zbir_cifara_str: string = "Zbir cifara unetog broja je:".@cast_to($zbir_cifara, $string_t);
@cput($zbir_cifara_str);

cond($zbir_cifara > 10) {
	dec $zbir_cifara_str: string = "Zbir cifara unetog broja je veci od 10";
	@cput($zbir_cifara_str);
}

cond($zbir_cifara < 10) {
	dec $zbir_cifara_str: string = "Zbir cifara unetog broja je manji od 10";
	@cput($zbir_cifara_str);
}
