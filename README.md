# Meshwell
<p align="center">
  <img src=https://raw.githubusercontent.com/simbilod/meshwell/main/meshwell.png
 width="300" height="300">
</p>

---

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23430914.svg)](https://doi.org/10.5281/zenodo.23430914)

Robust, efficient Python-based 2.5D meshing.

## Fork for gf180-tcad

This is [mithro/meshwell](https://github.com/mithro/meshwell), a fork of
[simbilod/meshwell](https://github.com/simbilod/meshwell) (forked at upstream `main`
[b6d5ccd](https://github.com/simbilod/meshwell/commit/b6d5ccd5293312e99c91686cd6f010ca7bda5e15))
maintained for [gf180-tcad](https://github.com/mithro/gf180-tcad), which compares TCAD against
the PDK SPICE models for GF180MCU 5V devices. gf180-tcad's dev-HEAD TCAD image runs meshwell
with gmsh's development HEAD (5.0), whose default MSH 4.2 output meshio cannot read back; the
fork carries the fix.

- All work happens on `gf180/<topic>` branches with pull requests inside this fork (base
  `mithro/meshwell:main`).
- Upstream (simbilod/meshwell) is **read-only** for this fork: no pushes, pull requests, issues
  or comments are made there.
- Fork CI runs only `Tests` (`.github/workflows/test_code.yml`) on GitHub-hosted runners with no
  secrets. The upstream workflows that publish (`release.yml` to PyPI, `pages.yml`), the Codecov
  upload and `dependabot.yml` are deleted, because this fork never releases or publishes.
- The fork keeps the upstream licence (GPL-3.0-or-later, as `CITATION.cff` states; `LICENSE` is
  the GPL version 3 text).

## 🧱 Key Features

* Preprocessing of [Shapely](https://shapely.readthedocs.io/en/stable/)-based inputs:
  * automated curve fitting for seamless curvilinear meshing
  * prismatic or tetrahedral elements
* Simple CAD interface to [OpenCASCADE](https://dev.opencascade.org/)
* Simple meshing interface to [GMSH](https://gmsh.info/)
* Remeshing utilities, including [MMG](https://github.com/MmgTools/MMG)

## 📦 Installation

```bash
pip install meshwell
```

## 📖 Documentation

For more information and examples, visit the [Documentation Site](https://github.com/simbilod/meshwell/actions/workflows/pages.yml).
