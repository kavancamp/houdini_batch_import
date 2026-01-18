import hou 

# Declare variables
# Ask the user for the files
default_directory = hou.text.expandString('$HIP')

select_directory = hou.ui.selectFile(start_directory=default_directory, 
    title="Select files to import", 
    file_type=hou.fileType.Geometry, 
    multiple_select=True
    )
if select_directory:
    select_directory = select_directory.split(';')
    
    obj = hou.node('/obj')
    geo_node = obj.createNode('geo', node_name= 'tempGeo')
    merge_node = geo_node.createNode('merge', node_name= 'MergeAll')
    add_to_merge = 0
    
    for item in select_directory:
        item = item.strip()
        asset = item.split('/')
        object = asset[-1].split('.')
        
        
        if object[-1] == 'abc':
            loader = geo_node.createNode('alembic', node_name=object[0])
            loader.parm('fileName').set(item)
            
            unpack_node = geo_node.createNode('unpack', node_name=object[0] + '_unpack')
            unpack_node.setInput(0, loader)

            source_node = unpack_node
            
        else:
            loader = geo_node.createNode('file', node_name=object[0])
            loader.parm('file').set(item)
            
            source_node = loader
            
            
        # Transform and set scale to 0.01
        xform_node = geo_node.createNode(
            'xform',
            node_name=object[0] + '_xform'
        )
        xform_node.parm('scale').set(0.01)
        xform_node.setInput(0, source_node)
        
        # Material node
        mat_node = geo_node.createNode(
            'material',
            node_name=object[0] + '_mat'
        )
        mat_node.setInput(0, xform_node)
    
        # merge
        merge_node.setNextInput(mat_node)
        
    null = geo_node.createNode("null", node_name="_OUT_")
    null.setInput(0, merge_node)
    null.setDisplayFlag(True)
    null.setRenderFlag(True)
    
    geo_node.layoutChildren()   
    
else:
    hou.ui.displayMessage("Check again: no valid file was selected", buttons=('OK', ))
    
# Ask the user for the files
# Create geometry node
# File node for FBX and OBJ, BGEO
# If Alembic use an Alembic loader
# Transform and set scale to 0.01
# Add material node
# Merge node