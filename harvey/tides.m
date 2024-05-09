m = msh('fort.14');
m = Make_f15(m,  '23-Sep-2017 12:00', '2-Sep-2017 12:00', 2, 'const', 'major8','tidal_database','h_tpxo9.v1.nc');

write(m, 'tides', 'f15');