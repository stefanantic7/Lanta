use cget, cput;
use cast_to;
use str_length, str_char_at, str_is_alpha, str_is_digit, str_split, str_to_upper, str_equals;
use array_size, array_get;

dec $string_t: string = "string";
dec $int_t: string = "int";

decfun solve($n:int): do {
	dec $unesite_text: string = "Unesite tekst:";
	dec $tekst: string = @cget($unesite_text);
	dec $novi_tekst: string = "";

	dec $index: int = 0;
	dec $rec: string = "";
	dec $char: string = "";


	dec $c1: string = " ";
	dec $c2: string = "\n";
	dec $c3: string = "\t";
	dec $c4: string = ".";
	dec $c5: string = ",";
	dec $c6: string = "?";
	dec $c7: string = "!";


	loond($index < @str_length($tekst)) {
		dec $char: string = @str_char_at($tekst, $index);

		cond( (@str_equals($char,$c1)==1) || (@str_equals($char,$c2)==1) || (@str_equals($char,$c3)==1) || (@str_equals($char,$c4)==1) || (@str_equals($char,$c5)==1) || (@str_equals($char,$c6)==1) || (@str_equals($char,$c7)==1) ) {
			cond(@str_length($rec) > $n) {
				dec $rec: string = @str_to_upper($rec);
			}
			dec $novi_tekst: string = $novi_tekst.$rec.$char;

			dec $rec: string = "";
		}

		cond( (@str_equals($char,$c1)==0) && (@str_equals($char,$c2)==0) && (@str_equals($char,$c3)==0) && (@str_equals($char,$c4)==0) && (@str_equals($char,$c5)==0) && (@str_equals($char,$c6)==0) && (@str_equals($char,$c7)==0) ) {
			dec $rec: string = $rec.$char;
		}

		dec $index: int = $index + 1;
	}

	cond(@str_length($rec) > $n) {
		dec $rec: string = @str_to_upper($rec);
	}
	
	dec $result_tekst: string = $novi_tekst.$rec; 
	@cput($result_tekst);
}

dec $unesite_n_str: string = "Unesite n: ";
dec $n_str: string = @cget($unesite_n_str);
dec $n: int = @cast_to($n_str, $int_t);
@solve($n);

