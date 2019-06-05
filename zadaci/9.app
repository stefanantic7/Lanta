##
Napisati program koji za unteti tekst ispisuje isti taj tekst ali tako da svaku reč dužu od n
karaktera, broj n se dobija kao parametar, ispisuje sa svim velikim slovima, ostale reči ispisuje
onako kako su unete. Reči su razdvojene razmacima i interpunkcijskim znacima (.,?!).
##
use cget, cput;
use cast_to;
use str_length, str_char_at, str_is_alpha, str_is_digit, str_split, str_replace, str_to_upper;
use array_size, array_get;

decfun solve($n:int): do {
	dec $tekst: string = @cget("Unesite tekst: ");
	dec $novi_tekst: string = "";

	dec $index: int = 0;
	dec $rec: string = "";
	dec $char: string = "";

	loond($index < @array_size($tekst)) {
		$char = @str_char_at($tekst, $index);

		cond($char == " " || $char == "\n" || $char == "\t" || $char == "." || $char == "," || $char == "?" || $char == "!") {
			cond(@str_length($rec) > $n) {
				$rec = @str_to_upper($rec);
			}
			$novi_tekst = $novi_tekst.$rec.$char;

			$rec = "";
		}

		cond($char != " " && $char != "\n" && $char != "\t" && $char != "." && $char != "," && $char != "?" && $char != "!") {
			$rec = $rec.$char;
		}

		$index = $index + 1;
	}

	cond(@str_length($rec) > $n) {
		$rec = @str_to_upper($rec);
	}
	
	@cput($novi_tekst.$rec);
}

dec $n: int = @cast_to(@cget("Unesite n: "), "int")
@solve($n);

