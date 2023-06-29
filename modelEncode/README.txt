
draco_encoder.exe -i export_0.obj -o export_0.drc

draco_encoder.exe -i export_5.obj -o export_5.drc

draco_encoder.exe -i export_0.ply -o export_0.drc -cl 10

draco_encoder.exe -i export_0.ply -o export_0.drc -cl 10 -qp 11 -qt 10 -qn 10 -qg 8

-cl 10	->	options.compression_level = 10;
-qp 11	->	options.pos_quantization_bits = 11;
-qt 10	->	options.tex_coords_quantization_bits = 10;
-qn 10	->	options.normals_quantization_bits = 10;
-qg 8	->	options.generic_quantization_bits = 8;