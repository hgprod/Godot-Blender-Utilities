@tool
extends EditorPlugin

var curve_import

func _enter_tree() -> void:
	curve_import = preload("curve_import.gd").new()
	add_import_plugin(curve_import)

func _exit_tree() -> void:
	remove_import_plugin(curve_import)
	curve_import = null
