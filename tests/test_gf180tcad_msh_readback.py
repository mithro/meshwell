# SPDX-License-Identifier: GPL-3.0-or-later
"""meshwell's meshio read-back of 2D meshes under gmsh 4.15.2 and gmsh 5.0 (mithro/meshwell fork).

gmsh 5 writes MSH 4.2 by default, which meshio 5.3.5 cannot read (meshwell/msh_compat.py). The
read-back must give the same mesh under both: the expected values below are those of gmsh 4.15.2
(PyPI), and the fork's CI runs this module under gmsh 4.15.2 and under the gmsh 5.0.0.dev20261018
snapshot (gmsh master c020e8f4) that gf180-tcad's dev-HEAD image uses.

Added for gf180-tcad (https://github.com/mithro/gf180-tcad).
"""

from __future__ import annotations

import gmsh
import pytest
from shapely.geometry import box

from meshwell.orchestrator import generate_mesh
from meshwell.polysurface import PolySurface

GMSH_MAJOR = int(gmsh.__version__.split(".")[0])


def _summary(m) -> dict:
    return {
        "points": len(m.points),
        "cells": sorted([c.type, len(c.data)] for c in m.cells),
        "field_data": {k: [int(x) for x in v] for k, v in sorted(m.field_data.items())},
        "cell_sets": {
            k: sorted(len(a) for a in v) for k, v in sorted(m.cell_sets.items())
        },
    }


SCENES = {
    "square": (
        lambda: [
            PolySurface(polygons=box(0, 0, 1, 1), physical_name="sq", mesh_order=1)
        ],
        0.5,
        {
            "points": 12,
            "cells": [["line", 2]] * 4 + [["triangle", 14]],
            "field_data": {"sq": [1, 2], "sq___None": [1, 1]},
            "cell_sets": {
                "gmsh:bounding_entities": [2, 2, 2, 2, 4],
                "sq": [0, 0, 0, 0, 14],
                "sq___None": [0, 2, 2, 2, 2],
            },
        },
    ),
    "two_layers": (
        lambda: [
            PolySurface(polygons=box(0, 0, 2, 1), physical_name="bottom", mesh_order=1),
            PolySurface(polygons=box(0, 1, 2, 1.5), physical_name="top", mesh_order=2),
        ],
        0.1,
        {
            "points": 402,
            "cells": [["line", 5], ["line", 5], ["line", 10], ["line", 10]]
            + [["line", 20]] * 3
            + [["triangle", 248], ["triangle", 484]],
            "field_data": {
                "bottom": [1, 2],
                "bottom___None": [2, 1],
                "bottom___top": [1, 1],
                "top": [2, 2],
                "top___None": [3, 1],
            },
            "cell_sets": {
                "bottom": [0] * 8 + [484],
                "bottom___None": [0] * 6 + [10, 10, 20],
                "bottom___top": [0] * 8 + [20],
                "gmsh:bounding_entities": [2] * 7 + [4, 4],
                "top": [0] * 8 + [248],
                "top___None": [0] * 6 + [5, 5, 20],
            },
        },
    ),
}


@pytest.mark.parametrize("scene", sorted(SCENES))
def test_2d_mesh_reads_back_as_with_gmsh_4_15(scene: str) -> None:
    entities, size, expected = SCENES[scene]
    m = generate_mesh(
        entities(), dim=2, default_characteristic_length=size, verbosity=0
    )
    assert _summary(m) == expected


@pytest.mark.skipif(GMSH_MAJOR < 5, reason="MSH 4.2 exists from gmsh 5")
def test_explicit_msh_4_2_still_reads_back_and_is_kept(tmp_path) -> None:
    """gmsh_version=4.2 is honoured for the caller's file; only the meshio read-back uses 4.1."""
    entities, size, expected = SCENES["square"]
    out = tmp_path / "mesh.msh"
    m = generate_mesh(
        entities(),
        dim=2,
        output_mesh=out,
        default_characteristic_length=size,
        verbosity=0,
        gmsh_version=4.2,
    )
    assert _summary(m) == expected
    assert out.read_text().splitlines()[1].split()[0] == "4.2"
    assert gmsh.option.getNumber("Mesh.MshFileVersion") == 4.2


def test_default_msh_version_is_4_1(tmp_path) -> None:
    """Without gmsh_version, meshwell writes MSH 4.1 (gmsh 4's default), also under gmsh 5."""
    entities, size, _ = SCENES["square"]
    out = tmp_path / "mesh.msh"
    generate_mesh(
        entities(),
        dim=2,
        output_mesh=out,
        default_characteristic_length=size,
        verbosity=0,
    )
    assert out.read_text().splitlines()[1].split()[0] == "4.1"
    assert gmsh.option.getNumber("Mesh.MshFileVersion") == 4.1
