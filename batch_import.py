import hou
default_directory = hou.text.expandString('$HIP')

default_scale = 0.01

choice = hou.ui.displayMessage(
    "Use default import scale (0.01)?",
    buttons=("Yes", "No", "Cancel"),
    default_choice=0,
    close_choice=2,
    title="Import Scale"
)

if choice == 2:  # Cancel
    raise hou.Error("Import cancelled by user.")

if choice == 0:
    import_scale = default_scale
else:
    # Ask for custom scale
    button, scale_str = hou.ui.readInput(
        "Enter custom import scale:",
        buttons=("OK", "Cancel"),
        initial_contents=str(default_scale),
        title="Custom Scale"
    )

    if button != 0:
        raise hou.Error("Import cancelled by user.")

    try:
        import_scale = float(scale_str.strip())
    except ValueError:
        hou.ui.displayMessage(
            f"'{scale_str}' is not a valid number.\nUsing default scale (0.01).",
            buttons=("OK",)
        )
        import_scale = default_scale


# Ask user for files 
select_directory = hou.ui.selectFile(
    start_directory=default_directory,
    title="Select files to import",
    file_type=hou.fileType.Geometry,
    multiple_select=True
)

if select_directory:
    select_directory = select_directory.split(';')

    obj = hou.node('/obj')
    geo_node = obj.createNode('geo', node_name='tempGeo')
    merge_node = geo_node.createNode('merge', node_name='MergeAll')

    for item in select_directory:
        item = item.strip()
        asset = item.split('/')
        obj_parts = asset[-1].split('.')
        base_name = obj_parts[0]
        ext = obj_parts[-1].lower()

        if ext == 'abc':
            loader = geo_node.createNode('alembic', node_name=base_name)
            loader.parm('fileName').set(item)

            unpack_node = geo_node.createNode('unpack', node_name=base_name + '_unpack')
            unpack_node.setInput(0, loader)

            source_node = unpack_node
        else:
            loader = geo_node.createNode('file', node_name=base_name)
            loader.parm('file').set(item)

            source_node = loader

        # Transform and set scale from UI
        xform_node = geo_node.createNode('xform', node_name=base_name + '_xform')
        xform_node.parm('scale').set(import_scale)
        xform_node.setInput(0, source_node)

        # Material node
        mat_node = geo_node.createNode('material', node_name=base_name + '_mat')
        mat_node.setInput(0, xform_node)

        # Merge
        merge_node.setNextInput(mat_node)

    out_null = geo_node.createNode("null", node_name="_OUT_")
    out_null.setInput(0, merge_node)
    out_null.setDisplayFlag(True)
    out_null.setRenderFlag(True)

    geo_node.layoutChildren()

else:
    hou.ui.displayMessage("Check again: no valid file was selected", buttons=('OK',))

# Ask the user for the files
# Create geometry node
# File node for FBX and OBJ, BGEO
# If Alembic use an Alembic loader
# Transform and set scale to 0.01
# Add material node
# Merge node