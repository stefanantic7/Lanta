use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;
use str_length, str_char_at, str_is_alpha, str_is_digit;

dec $string_t: string = "string";
dec $int_t: string = "int";

dec $unesite_text: string = "Unesite text: "; 
dec $text: string = @cget($unesite_text);
dec $nula: int = 0;
dec $previous_char: string = @str_char_at($text, $nula);
dec $current_char: string = "";
dec $index: int = 1;
dec $result: string = "";

loond($index < @str_length($text)) {
	dec $current_char: string = @str_char_at($text, $index);
	cond( (@str_is_alpha($previous_char) == 1)  && (@str_is_digit($current_char) == 1) ) {
		dec $result: string = $result.$previous_char."*".$current_char;
	}
	cond( (@str_is_digit($previous_char) == 1) && (@str_is_alpha($current_char) == 1) ) {
		dec $result: string = $result.$previous_char."#".$current_char;
	}
	cond( (@str_is_digit($previous_char) == 1) && (@str_is_digit($current_char) == 1) ) {
		dec $result: string = $result.$previous_char.$current_char;
	}
	cond( (@str_is_alpha($previous_char) == 1) && (@str_is_alpha($current_char) == 1) ) {
		dec $result: string = $result.$previous_char.$current_char;
	}
	dec $previous_char: string = $current_char;
	dec $index: int = $index + 1;
}

@cput($result);