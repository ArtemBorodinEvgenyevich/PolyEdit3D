import os
from pathlib import Path
from enum import Enum, unique


_ = Path(os.path.dirname(__file__))

project_root = _.parent.parent
source_root = os.path.join(project_root, 'PolyEdit3D')

resources_path = os.path.join(source_root, "Resources")

shaders_path = os.path.join(resources_path, "Shaders")
shader_entity_basic_fragment = os.path.join(shaders_path, "EntityBasicFrag.glsl")
shader_entity_basic_vertex = os.path.join(shaders_path, "EntityBasicVert.glsl")
shader_coord_dots_vertex = os.path.join(shaders_path, "CoordDotsVert.glsl")
shader_coord_dots_fragment = os.path.join(shaders_path, "CoordDotsFrag.glsl")
shader_coord_lines_vertex = os.path.join(shaders_path, "CoordLinesVert.glsl")
shader_coord_lines_fragment = os.path.join(shaders_path, "CoordLinesFrag.glsl")



icons_path = os.path.join(resources_path, 'Icons')
btn_wireframe_ico = os.path.join(icons_path, "WireIco.png")


@unique
class AppPaths(Enum):
    """Set of project's paths represented as enums."""
    PROJECT_ROOT = project_root
    SOURCE_ROOT = source_root

    SHADERS_PATH = shaders_path
    SHADER_ENTITY_BASIC_FRAGMENT = shader_entity_basic_fragment
    SHADER_ENTITY_BASIC_VERTEX = shader_entity_basic_vertex
    SHADER_COORD_DOTS_FRAGMENT = shader_coord_dots_fragment
    SHADER_COORD_DOTS_VERTEX = shader_coord_dots_vertex
    SHADER_COORD_LINES_FRAGMENT = shader_coord_lines_fragment
    SHADER_COORD_LINES_VERTEX = shader_coord_lines_vertex

    BTN_WIREFRAME_ICON = btn_wireframe_ico





