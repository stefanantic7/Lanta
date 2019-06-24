use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;
use str_length, str_char_at, str_is_alpha, str_is_digit;

dec $string_t: string = "string";
dec $int_t: string = "int";

dec $unesite_rec: string = "Unesite rec:";
dec $rec: string = @cget($unesite_rec);
dec $index_1: int = 0;
dec $index_2: int = 0;
dec $index_space: int = 0;
dec $row: string = "";
dec $previous_row: string = "";

cond(@str_length($rec) % 2 == 0) {
	dec $index_1: int = (@str_length($rec) // 2) - 1;
	dec $index_2: int = $index_1 + 1;

	loond($index_1 >= 0) {
		dec $index_space: int = 0;
		dec $row: string = "";

		dec $previous_row: string = @str_char_at($rec, $index_1).$previous_row.@str_char_at($rec, $index_2);

		loond($index_space < $index_1) {
			dec $row: string = $row." ";
			dec $index_space: int = $index_space + 1;
		}


		dec $row: string = $row.$previous_row;

		@cput($row);
		dec $index_1: int = $index_1 - 1;
		dec $index_2: int = $index_2 + 1;	
	}
}

cond(@str_length($rec) % 2 != 0) {
	dec $index_1: int = @str_length($rec) // 2;
	dec $row: string = "";
	dec $index_space: int = 0;
	dec $previous_row: string = @str_char_at($rec, $index_1);
	loond($index_space < $index_1) {
		dec $row: string = $row." ";
		dec $index_space: int = $index_space + 1;
	}
	dec $row: string = $row.$previous_row;
	@cput($row);
	
	dec $index_1: int = $index_1 - 1;
	dec $index_2: int = $index_1 + 2;

	loond($index_1 >= 0) {
		dec $index_space: int = 0;

		dec $previous_row: string = @str_char_at($rec, $index_1).$previous_row.@str_char_at($rec, $index_2);

		dec $row: string = "";
		loond($index_space < $index_1) {
			dec $row: string = $row." ";
			dec $index_space: int = $index_space + 1;
		}

		dec $row:string = $row.$previous_row;
		@cput($row);

		dec $index_1: int = $index_1 - 1;
		dec $index_2: int = $index_2 + 1;	
	}
}