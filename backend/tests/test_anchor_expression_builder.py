from app.services.anchor_expression_builder import build_anchor_expression_batch


def test_build_anchor_expression_batch_surfaces_photonics_anchor_adjacent_and_upstream() -> None:
    batch = build_anchor_expression_batch(
        [
            {
                "kept_artifacts": [
                    {
                        "artifact_id": "nvda_1",
                        "source_class": "company_release",
                        "issuing_company_name": "NVIDIA",
                        "title": "NVIDIA Announces Spectrum-X Photonics Networking Switches",
                        "body_text": "The ecosystem includes Coherent and Lumentum for AI factories.",
                        "category_tags": ["photonics", "AI networking"],
                    },
                    {
                        "artifact_id": "lite_1",
                        "source_class": "company_release",
                        "issuing_company_name": "Lumentum",
                        "title": "Lumentum Expands U.S. Manufacturing for AI-Driven Co-Packaged Optics",
                        "body_text": "Lumentum is a primary supplier of ultra-high-power lasers for CPO.",
                        "category_tags": ["InP", "co-packaged optics"],
                    },
                ],
                "review_artifacts": [
                    {
                        "artifact_id": "cohr_1",
                        "source_class": "company_release",
                        "issuing_company_name": "Coherent",
                        "title": "6-inch InP Scalable Wafer Fabs for AI Transceivers",
                        "body_text": "Coherent expands capacity in its fabs for indium phosphide devices.",
                        "category_tags": ["InP", "capacity expansion"],
                    },
                    {
                        "artifact_id": "jx_1",
                        "source_class": "company_release",
                        "issuing_company_name": "JX Advanced Metals",
                        "title": "Notice Regarding Capital Investment for Increased Production of Crystal Materials",
                        "body_text": "",
                        "category_tags": ["InP", "capacity expansion"],
                    },
                ],
            }
        ],
        profile_name="photonics",
    )

    assert batch["metrics"]["anchor_expression_count"] == 3
    names = [item["canonical_entity_name"] for item in batch["anchors"]]
    assert names == ["Lumentum", "Coherent", "JX Advanced Metals"]
    assert batch["anchors"][0]["anchor_role"] == "anchor_expression"
    assert batch["anchors"][1]["anchor_role"] == "adjacent_anchor"
    assert batch["anchors"][2]["anchor_role"] == "upstream_dependency"


def test_build_anchor_expression_batch_excludes_system_driver_rows() -> None:
    batch = build_anchor_expression_batch(
        [
            {
                "kept_artifacts": [
                    {
                        "artifact_id": "nvda_1",
                        "source_class": "company_release",
                        "issuing_company_name": "NVIDIA",
                        "title": "NVIDIA Announces Spectrum-X Photonics Networking Switches",
                        "body_text": "AI factories and photonics ecosystem",
                        "category_tags": ["photonics", "AI networking"],
                    }
                ],
                "review_artifacts": [],
            }
        ],
        profile_name="photonics",
    )

    assert batch["anchors"] == []


def test_build_anchor_expression_batch_marks_axt_as_upstream_dependency() -> None:
    batch = build_anchor_expression_batch(
        [
            {
                "kept_artifacts": [
                    {
                        "artifact_id": "axt_1",
                        "source_class": "company_filing",
                        "issuing_company_name": "AXT",
                        "title": "AXT INC_March 31, 2025",
                        "body_text": "Demand for indium phosphide substrates and optical networking components increased with AI data center deployments.",
                        "category_tags": ["InP", "photonics", "AI infrastructure"],
                    }
                ],
                "review_artifacts": [],
            }
        ],
        profile_name="photonics",
    )

    assert batch["anchors"][0]["canonical_entity_name"] == "AXT"
    assert batch["anchors"][0]["anchor_role"] == "upstream_dependency"
