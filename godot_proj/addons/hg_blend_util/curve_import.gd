@tool extends EditorImportPlugin

func _get_importer_name():
	return "hg_prod.curve_import"

func _get_visible_name() -> String:
	return "Blender Curve Import"

func _get_recognized_extensions() -> PackedStringArray:
	return ["godot_curve"]

func _get_save_extension() -> String:
	return "tscn"

func _get_resource_type() -> String:
	return "PackedScene"

func _get_priority() -> float:
	return 1.0

func _get_preset_count() -> int:
	return 0

func _get_import_order() -> int:
	return 0

func _get_import_options(path: String, preset_index: int) -> Array[Dictionary]:
	return []

func _import(source_file: String, save_path: String, options: Dictionary, platform_variants: Array[String], gen_files: Array[String]) -> Error:
	var file = FileAccess.open(source_file, FileAccess.READ)
	if file == null:
		return FileAccess.get_open_error()
	var data_text := file.get_as_text()
	var data := JSON.parse_string(data_text)
	var is_single := data["curve_list"].size() == 1 as bool
	var scene := PackedScene.new()
	if is_single:
		var path := _create_path(data["curve_list"][0])
		scene.pack(path)
	else:
		var node := Node3D.new()
		node.name = "PathGroup"
		for curve_data in data["curve_list"]:
			var path := _create_path(curve_data)
			node.add_child(path)
			path.owner = node
		scene.pack(node)
	return ResourceSaver.save(scene, "%s.%s" % [save_path, _get_save_extension()])

func _create_path(obj: Dictionary) -> Path3D:
	var path := Path3D.new()
	path.name = obj["name"]
	path.curve = _create_shape(obj["data"])
	path.curve.closed = obj["is_closed"]
	return path

func _create_shape(obj: Array) -> Curve3D:
	var curve := Curve3D.new()
	for item in obj:
		var pos := _as_vec3(item["pos"])
		var left := _as_vec3(item["left"])
		var right := _as_vec3(item["right"])
		curve.add_point(pos, left - pos, right - pos)
		curve.set_point_tilt(curve.point_count-1, item["tilt"])
	return curve

func _as_vec3(obj: Array) -> Vector3:
	return Vector3(obj[0], obj[2], -obj[1])
