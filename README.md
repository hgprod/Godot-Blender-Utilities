This is the Happy Golem Godot/Blender Utility Archive.

Everything here is open source (CC0), and released as is.

If using the items in the ditribution, the .py needs to be installed as a Blender addon. The folder needs to go into the godot project addons folder.

The only item currently in this package is a set of import/export plugins to convert a blender bezier curve to a godot path. Only Bezier curves will be exported with blender, all others will be ignored. Godot plugin will import the path as it was created. Tilts will be transferred with the path.

All positions will be exported without considering the object transform. If blender transforms are not applied, adjustments may need to be made in godot.
