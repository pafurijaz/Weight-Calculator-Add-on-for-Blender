# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "Weight Calculator Add-on",
    "blender": (3, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "pafurijaz",
    "description": "A Blender add-on to calculate the weight of selected mesh objects based on their material.",
}

import bpy
from mathutils import Matrix
import bmesh

# Define the materials we support
materials = [
    "iron", "steel", "stainless_steel", "aluminum", "copper", "brass", "bronze",
    "titanium", "gold", "silver", "lead", "zinc", "magnesium", "nickel",
    "plastic", "wood", "concrete", "glass", "brick", "marble", "granite",
    "carbon_fiber", "foam", "rubber", "uranium", "mercury", "diamond"
]

def is_solid_mesh(obj):
    if obj.type != 'MESH':
        return False
    
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Check for solid faces (faces that are not split or non-planar)
    for face in bm.faces:
        if len(face.verts) < 3:
            continue
        if face.calc_area() == 0:
            return False
    
    # Check for manifold edges (edges shared by exactly two faces)
    for edge in bm.edges:
        if not edge.is_manifold:
            return False
    
    bm.free()
    return True

def get_mesh_volume(mesh, unit_conversion_factor):
    volume = 0.0
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    for face in bm.faces:
        centroid = face.calc_center_median()
        normal = face.normal
        area = face.calc_area()
        
        # Use a plane equation to calculate the signed distance from the origin
        A, B, C, D = normal[0], normal[1], normal[2], -centroid.dot(normal)
        volume += abs(D) * area / 3
    
    bm.free()
    return volume * unit_conversion_factor

def get_material_density(material_name):
    material_densities = {
        "iron": 7850,
        "steel": 7850,
        "stainless_steel": 8000,
        "aluminum": 2700,
        "copper": 8960,
        "brass": 8500,
        "bronze": 8730,
        "titanium": 4500,
        "gold": 19300,
        "silver": 10500,
        "lead": 11340,
        "zinc": 7130,
        "magnesium": 1738,
        "nickel": 8908,
        "plastic": 1200,
        "wood": 600,
        "concrete": 2400,
        "glass": 2500,
        "brick": 1922,
        "marble": 2700,
        "granite": 2691,
        "carbon_fiber": 1800,
        "foam": 100,
        "rubber": 1500,
        "uranium": 19050,
        "mercury": 13534,
        "diamond": 3500
    }
    return material_densities.get(material_name.lower(), 1000)

def get_custom_material_density():
    # Retrieve the custom density from the scene property
    return bpy.context.scene.custom_density

def get_custom_volume(unit_conversion_factor):
    # Retrieve the custom volume from the scene property
    return bpy.context.scene.custom_volume * unit_conversion_factor

def get_mesh_weight(mesh, use_custom_density=False, use_custom_volume=False, unit_conversion_factor=1.0, density_conversion_factor=1.0):
    if use_custom_volume:
        volume = get_custom_volume(unit_conversion_factor)
    else:
        volume = get_mesh_volume(mesh, unit_conversion_factor)
    
    if use_custom_density:
        density = get_custom_material_density()
    else:
        density = get_material_density(bpy.context.scene.material_type)
    
    return volume * density * density_conversion_factor

class OBJECT_PT_weight_calculator(bpy.types.Panel):
    bl_label = "Weight Calculator"
    bl_idname = "OBJECT_PT_weight_calculator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(scene, "material_type")
        
        # Option to use custom density
        row = layout.row()
        row.prop(scene, "use_custom_density", text="Use Custom Density")
        if scene.use_custom_density:
            row = layout.row()
            row.prop(scene, "custom_density", text="Density (kg/m^3)")
        
        # Option to use custom volume
        row = layout.row()
        row.prop(scene, "use_custom_volume", text="Use Custom Volume")
        if scene.use_custom_volume:
            row = layout.row()
            row.prop(scene, "custom_volume", text="Volume (m^3)")
        
        # Unit system selection
        row = layout.row()
        row.prop(scene, "unit_system", text="Unit System")
        
        # Unit selection
        row = layout.row()
        row.prop(scene, "length_unit", text="Length Unit")
        
        # New button for volume calculation
        row = layout.row()
        row.operator("object.volume_calculate", text="Calculate Volume")
        
        # Move the "Calculate Weight" button to the fourth row
        row = layout.row()
        row.operator("object.weight_calculate", text="Calculate Weight")

class OBJECT_OT_calculate_weight(bpy.types.Operator):
    bl_idname = "object.weight_calculate"
    bl_label = "Calculate Weight"

    def execute(self, context):
        # Check if any objects are selected
        if not bpy.context.selected_objects:
            self.report({'ERROR'}, "No object is selected. Please select a valid mesh object.")
            return {'CANCELLED'}
        
        # Filter to get only mesh objects that are solid
        solid_meshes = [obj for obj in context.selected_objects if is_solid_mesh(obj)]
        
        if not solid_meshes:
            self.report({'ERROR'}, "No solid mesh objects selected.")
            return {'CANCELLED'}

        use_custom_density = context.scene.use_custom_density
        use_custom_volume = context.scene.use_custom_volume
        
        # Get unit conversion factors
        unit_conversion_factor, density_conversion_factor, weight_unit, volume_unit = get_unit_conversion_factors(context.scene.unit_system, context.scene.length_unit)
        
        # Calculate and report the weight using the mesh data
        total_weight = 0.0
        for obj in solid_meshes:
            mesh = obj.data
            weight = get_mesh_weight(mesh, use_custom_density, use_custom_volume, unit_conversion_factor, density_conversion_factor)
            total_weight += weight
        
        self.report({'INFO'}, f"Total Weight: {total_weight:.6f} {weight_unit}")
        
        return {'FINISHED'}

class OBJECT_OT_calculate_volume(bpy.types.Operator):
    bl_idname = "object.volume_calculate"
    bl_label = "Calculate Volume"

    def execute(self, context):
        # Check if any objects are selected
        if not bpy.context.selected_objects:
            self.report({'ERROR'}, "No object is selected. Please select a valid mesh object.")
            return {'CANCELLED'}
        
        # Filter to get only mesh objects that are solid
        solid_meshes = [obj for obj in context.selected_objects if is_solid_mesh(obj)]
        
        if not solid_meshes:
            self.report({'ERROR'}, "No solid mesh objects selected.")
            return {'CANCELLED'}

        # Get unit conversion factors
        unit_conversion_factor, density_conversion_factor, weight_unit, volume_unit = get_unit_conversion_factors(context.scene.unit_system, context.scene.length_unit)
        
        # Calculate and report the volume using the mesh data
        total_volume = 0.0
        for obj in solid_meshes:
            mesh = obj.data
            volume = get_mesh_volume(mesh, unit_conversion_factor)
            total_volume += volume
        
        self.report({'INFO'}, f"Total Volume: {total_volume:.6f} {volume_unit}")
        
        return {'FINISHED'}

def get_unit_conversion_factors(unit_system, length_unit):
    if unit_system == 'METRIC':
        if length_unit == 'MILLIMETERS':
            return 1e-9, 1e3, 'g', 'mm³'  # mm^3 to m^3, kg to g
        elif length_unit == 'CENTIMETERS':
            return 1e-6, 1e3, 'g', 'cm³'  # cm^3 to m^3, kg to g
        elif length_unit == 'METERS':
            return 1.0, 1.0, 'kg', 'm³'  # m^3 to m^3, kg to kg
    elif unit_system == 'IMPERIAL':
        if length_unit == 'INCHES':
            return 1.63871e-5, 35.27396, 'oz', 'in³'  # in^3 to m^3, kg to oz
        elif length_unit == 'FEET':
            return 0.0283168, 2.20462, 'lb', 'ft³'  # ft^3 to m^3, kg to lb
    return 1.0, 1.0, 'kg', 'm³'  # Default to no conversion

def register():
    bpy.utils.register_class(OBJECT_PT_weight_calculator)
    bpy.utils.register_class(OBJECT_OT_calculate_weight)
    bpy.utils.register_class(OBJECT_OT_calculate_volume)  # Register the new operator

    # Register the scene properties for material type, use custom density, and custom density value
    bpy.types.Scene.material_type = bpy.props.EnumProperty(
        name="Material Type",
        description="Select a material type to calculate its weight",
        items=[(mat, mat.capitalize(), "") for mat in materials],
        default="iron"
    )
    
    bpy.types.Scene.use_custom_density = bpy.props.BoolProperty(
        name="Use Custom Density",
        description="Enable custom density input",
        default=False
    )
    
    bpy.types.Scene.custom_density = bpy.props.FloatProperty(
        name="Density (kg/m^3)",
        description="Enter the custom material density in kg/m^3",
        min=1.0,
        default=2500.0  # Default to a reasonable value for most materials
    )
    
    bpy.types.Scene.use_custom_volume = bpy.props.BoolProperty(
        name="Use Custom Volume",
        description="Enable custom volume input",
        default=False
    )
    
    bpy.types.Scene.custom_volume = bpy.props.FloatProperty(
        name="Volume (m^3)",
        description="Enter the custom volume in m^3",
        min=0.0,
        default=1.0  # Default to a reasonable value
    )
    
    bpy.types.Scene.unit_system = bpy.props.EnumProperty(
        name="Unit System",
        description="Select the unit system",
        items=[
            ('METRIC', 'Metric', ''),
            ('IMPERIAL', 'Imperial', '')
        ],
        default='METRIC'
    )
    
    bpy.types.Scene.length_unit = bpy.props.EnumProperty(
        name="Length Unit",
        description="Select the length unit",
        items=[
            ('MILLIMETERS', 'Millimeters', ''),
            ('CENTIMETERS', 'Centimeters', ''),
            ('METERS', 'Meters', ''),
            ('INCHES', 'Inches', ''),
            ('FEET', 'Feet', '')
        ],
        default='MILLIMETERS'
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_weight_calculator)
    bpy.utils.unregister_class(OBJECT_OT_calculate_weight)
    bpy.utils.unregister_class(OBJECT_OT_calculate_volume)  # Unregister the new operator

    # Unregister the scene properties
    del bpy.types.Scene.material_type
    del bpy.types.Scene.use_custom_density
    del bpy.types.Scene.custom_density
    del bpy.types.Scene.use_custom_volume
    del bpy.types.Scene.custom_volume
    del bpy.types.Scene.unit_system
    del bpy.types.Scene.length_unit

# Register the classes
if __name__ == "__main__":
    register()