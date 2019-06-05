use cget, cput;
use cast_to;
use random;
use array_init, array_append, array_size, array_get;
use sqrt;
use is_integer;
use str_length, str_char_at, str_is_alpha, str_is_digit;

dec $rec: string = @cget("Unesite rec: ");
dec $index_1: int = 0;
dec $index_2: int = 0;
dec $index_space: int = 0;
dec $row: string = "";

cond(@str_length($rec) % 2 == 0) {
	$index_1 = (@str_length($rec) // 2) - 1;
	$index_2 = $index_1 + 1;

	loond($index_1 >= 0) {
		$index_space = 0;
		$row = "";
		loond($index_space < $index_1) {
			$row = $row." ";
			$index_space = $index_space + 1;
		}

		$row = $row.@str_char_at($rec, $index_1).@str_char_at($rec, $index_2);
		@cput($row);

		$index_1 = $index_1 - 1;
		$index_2 = $index_2 + 1;	
	}
}

cond(@str_length($rec) % 2 != 0) {
	$index_1 = @str_length($rec) // 2;
	$row = "";
	$index_space = 0;
	loond($index_space < $index_1) {
		$row = $row." ";
		$index_space = $index_space + 1;
	}
	$row = $row.@str_char_at($rec, $index_1);
	@cput($row);
	
	$index_1 = $index_1 - 1;
	$index_2 = $index_1 + 1;

	loond($index_1 >= 0) {
		$index_space = 0;
		$row = "";
		loond($index_space < $index_1) {
			$row = $row." ";
			$index_space = $index_space + 1;
		}

		$row = $row.@str_char_at($rec, $index_1).@str_char_at($rec, $index_2);
		@cput($row);

		$index_1 = $index_1 - 1;
		$index_2 = $index_2 + 1;	
	}
}