# SPDX-License-Identifier: GPL-3.0-or-later
"""Write MSH files that meshio can read back.

meshio (5.3.5, its latest release, equal to its git HEAD) reads MSH up to version 4.1. gmsh 5
writes MSH 4.2 by default (gmsh commit f3306764, "add MSH 4.2, now the default"), whose
``$Entities`` records end with lists of embedded entities (gmsh commit 51eba072, "add support for
embedded entities in MSH4.2"). meshio's 4.1 reader does not expect those lists and misreads the
records after the first one (for a 2D mesh: ``KeyError`` on a curve tag in
``meshio/gmsh/_gmsh41.py``, ``_read_elements``).

So meshwell writes MSH 4.1 unless the caller asks for another version (``gmsh_version``), and its
own in-memory meshio read-backs always use a version meshio reads.

Added in the mithro/meshwell fork for gf180-tcad (https://github.com/mithro/gf180-tcad).
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import gmsh

# The newest MSH version meshio reads.
MESHIO_MAX_MSH_VERSION = 4.1
# The MSH version meshwell writes when the caller does not ask for one: gmsh 4's default, so a
# file meshwell writes reads back with meshio under gmsh 4 and gmsh 5 alike.
DEFAULT_MSH_VERSION = MESHIO_MAX_MSH_VERSION


@contextlib.contextmanager
def meshio_readable_msh() -> Iterator[None]:
    """Cap ``Mesh.MshFileVersion`` at 4.1 for the ``gmsh.write`` calls inside, then restore it.

    A version of 4.1 or older (for example a ``gmsh_version=2.2`` asked for by the caller) is kept.
    """
    version = gmsh.option.getNumber("Mesh.MshFileVersion")
    if version > MESHIO_MAX_MSH_VERSION:
        gmsh.option.setNumber("Mesh.MshFileVersion", MESHIO_MAX_MSH_VERSION)
    try:
        yield
    finally:
        gmsh.option.setNumber("Mesh.MshFileVersion", version)
