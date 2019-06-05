use cget, cput;
use cast_to;
use str_length, str_char_at, str_is_alpha, str_is_digit, str_split, str_replace, str_to_upper;
use array_size, array_get;
use file_read;

dec $file_path: string = @cget("Unesite putanju: ");
dec $content: string = @file_read($file_path);
dec $reci_teksta: array = @str_split($content, " ");
dec $broj_reci: int = @cast_to(@cget("Unesite putanju: "), "int");
dec $kljucne_reci: array = @str_split(@cget("Unesite kljucne reci (odvojene zarezom): "), ",");
dec $rec: string = "";
dec $counter: int = 0;

dec $index_kljucne_reci: int = 0;
dec $index_reci_teksta: int = 0;

loond($index_kljucne_reci < @array_size($kljucne_reci)) {
	$rec = @array_get($kljucne_reci, $index_kljucne_reci);
	$counter = 0;
	$index_reci_teksta = 0;
	loond($index_reci_teksta < @array_size($reci_teksta)) {
		cond(@array_get($reci_teksta, $index_reci_teksta) == $rec) {
			$counter = $counter + 1;
		}
		$index_reci_teksta = $index_reci_teksta + 1;
	} 

	@cput($rec.": ".@cast_to($counter, "string"))

	$index_kljucne_reci = $index_kljucne_reci + 1;
}