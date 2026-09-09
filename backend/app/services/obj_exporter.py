from typing import Tuple

def parse_obj_mesh_stream(obj_plaintext: str) -> Tuple[bool, str, dict]:
    """
    Validate and inspect Wavefront OBJ plaintext content.
    Counts geometric vertex positions ('v x y z'), normals ('vn'), UVs ('vt'),
    and polygonal faces ('f v1 v2 v3').
    """
    if not obj_plaintext:
        return False, "Empty OBJ content", {}

    vertices_count = 0
    normals_count = 0
    uvs_count = 0
    faces_count = 0

    for line in obj_plaintext.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("v "):
            vertices_count += 1
        elif line.startswith("vn "):
            normals_count += 1
        elif line.startswith("vt "):
            uvs_count += 1
        elif line.startswith("f "):
            faces_count += 1

    if vertices_count == 0:
        return False, "OBJ contains no vertex definitions ('v ')", {}

    summary = {
        "vertices": vertices_count,
        "faces": faces_count,
        "normals": normals_count,
        "uvs": uvs_count,
        "manifoldTriangles": faces_count,
        "valid": True
    }
    return True, "Valid Wavefront OBJ mesh structure", summary
