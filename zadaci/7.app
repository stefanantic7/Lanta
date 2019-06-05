##
Napisati program koji za uneti tekst ispisuje isti taj tekst sa umetnutom tarabom (#) između
svakog uzastopnog pojavljivanja cifre i slova i zvezdicom (*) između svakog uzastopnog
pojavljivanja slova i cifre.
##

use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;
use str_length, str_char_at, str_is_alpha, str_is_digit;

dec $text: string = @cget("Unesite text: ");
dec $previous_char: string = @str_char_at($text, 0);
dec $current_char: string = "";
dec $index: int = 1;
dec $result: string = "";

loond($index < @str_length($text)) {
	$current_char = @str_char_at($text, $index);
	cond(@str_is_alpha($previous_char) && @str_is_digit($current_char)) {
		$result = $result.$previous_char."*".$current_char
	}
	cond(@str_is_digit($previous_char) && @str_is_alpha($current_char)) {
		$result = $result.$previous_char."#".$current_char	
	}
	cond(@str_is_digit($previous_char) && @str_is_digit($current_char)) {
		$result = $result.$previous_char.$current_char	
	}
	cond(@str_is_alpha($previous_char) && @str_is_alpha($current_char)) {
		$result = $result.$previous_char.$current_char	
	}
	$previous_char = $current_char;
	$index = $index + 1;
}

@cput($result);