# Photonics Dependency Graph v1

Purpose:

- convert the archive-backed photonics chronology into a deterministic chain graph
- make the inferred research path explicit:
  - `LITE`
  - `COHR`
  - `AAOI`
  - `AXTI`

Inputs:

- archive-backed workflow artifact:
  - `2026-03-22-aleabitoreddit-photonics-anchor-workflow-v1.json`

Nodes:

1. `Lumentum`
2. `Coherent`
3. `Applied Optoelectronics`
4. `AXT`

Edge types:

1. `adjacent_duopoly_context`
2. `levered_adjacent_expression`
3. `upstream_material_dependency`
4. `shared_inp_dependency`
5. `compared_against_anchor`

Boundary:

- this graph is an archive-backed interpretation artifact
- it is not a live supply-chain truth graph
- it encodes the reconstructed AleaBito path, not a general ontology
