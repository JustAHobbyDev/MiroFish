from app.services.anchor_first_blind_replay_builder import build_anchor_first_blind_replay_batch


def test_build_anchor_first_blind_replay_batch_marks_anchor_detection_but_not_hidden_chokepoint() -> None:
    payload = build_anchor_first_blind_replay_batch(
        [
            {
                "kept_artifacts": [
                    {
                        "artifact_id": "lite_1",
                        "source_class": "company_release",
                        "issuing_company_name": "Lumentum",
                        "title": "Lumentum Expands U.S. Manufacturing for AI-Driven Co-Packaged Optics",
                        "body_text": "Lumentum is a primary supplier of ultra-high-power lasers for CPO.",
                        "category_tags": ["InP", "co-packaged optics"],
                    }
                ],
                "review_artifacts": [
                    {
                        "artifact_id": "cohr_1",
                        "source_class": "company_release",
                        "issuing_company_name": "Coherent",
                        "title": "6-inch InP Scalable Wafer Fabs for AI Transceivers",
                        "body_text": "Coherent expands capacity in its fabs for indium phosphide devices.",
                        "category_tags": ["InP", "capacity expansion"],
                    }
                ],
            }
        ],
        profile_name="photonics",
        corpus_label="test_photonics",
    )

    assert payload["judgment"]["anchor_clue_detection"] == "pass"
    assert payload["judgment"]["adjacent_expression_surfacing"] == "pass"
    assert payload["judgment"]["hidden_chokepoint_recovery"] == "fail"
    assert payload["metrics"]["anchor_expression_names"] == ["Lumentum", "Coherent"]
