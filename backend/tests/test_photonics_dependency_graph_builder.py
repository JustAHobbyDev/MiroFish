from app.services.photonics_dependency_graph_builder import build_photonics_dependency_graph


def test_build_photonics_dependency_graph_maps_archive_roles_and_edges() -> None:
    payload = build_photonics_dependency_graph(
        {
            "artifact_id": "workflow_v1",
            "chronology": [
                {"expression": "LITE", "role": "anchor_expression"},
                {"expression": "COHR", "role": "adjacent_anchor"},
                {"expression": "AAOI", "role": "levered_adjacent_expression"},
                {"expression": "AXTI", "role": "hidden_upstream_chokepoint"},
            ],
        }
    )

    assert payload["metrics"] == {"node_count": 4, "edge_count": 5}
    assert [item["canonical_entity_name"] for item in payload["nodes"]] == [
        "Lumentum",
        "Coherent",
        "Applied Optoelectronics",
        "AXT",
    ]
    relation_types = {item["relation_type"] for item in payload["edges"]}
    assert "upstream_material_dependency" in relation_types
    assert "adjacent_duopoly_context" in relation_types
