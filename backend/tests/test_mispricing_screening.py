from app.services.mispricing_screening import (
    MispricingCandidate,
    MispricingSignals,
    OptionsExpressionSignals,
    score_mispricing_candidate,
    screen_candidates,
)


def test_score_mispricing_candidate_returns_two_scores_in_bounds():
    candidate = MispricingCandidate(
        name="MU LEAPS on packaging duration",
        thesis="Market underestimates how long advanced packaging stays tight.",
        underlying="MU",
        mispricing_type="variance_underpricing",
        posture="bullish_long_vol",
        preferred_expression="leaps_call",
        time_horizon="12-24m",
        mispricing_signals=MispricingSignals(
            hiddenness=4,
            recognition_gap=4,
            catalyst_clarity=3,
            propagation_asymmetry=4,
            duration_mismatch=5,
            evidence_quality=4,
            crowding_inverse=3,
            valuation_nonlinearity=4,
        ),
        options_expression_signals=OptionsExpressionSignals(
            convexity_need=4,
            tenor_alignment=5,
            vol_expansion_potential=4,
            downside_definedness=4,
            liquidity_path=4,
            implementation_simplicity=4,
            catalyst_timing_specificity=3,
        ),
    )

    result = score_mispricing_candidate(candidate)

    assert 0 <= result.mispricing.score_0_to_100 <= 100
    assert 0 <= result.options_fit.score_0_to_100 <= 100
    assert result.mispricing.band in {"critical", "high", "moderate", "emerging", "low"}
    assert result.options_fit.band in {"critical", "high", "moderate", "emerging", "low"}
    assert "MU LEAPS on packaging duration" in result.mispricing.explanation
    assert "MU LEAPS on packaging duration" in result.options_fit.explanation


def test_screen_candidates_preserves_order():
    candidates = [
        MispricingCandidate(
            name="Candidate A",
            thesis="A",
            underlying="AAA",
            mispricing_type="hidden_bottleneck",
            posture="bullish",
            preferred_expression="call_spread",
            time_horizon="6-12m",
            mispricing_signals=MispricingSignals(
                hiddenness=3,
                recognition_gap=3,
                catalyst_clarity=3,
                propagation_asymmetry=3,
                duration_mismatch=3,
                evidence_quality=3,
                crowding_inverse=3,
                valuation_nonlinearity=3,
            ),
            options_expression_signals=OptionsExpressionSignals(
                convexity_need=3,
                tenor_alignment=3,
                vol_expansion_potential=3,
                downside_definedness=3,
                liquidity_path=3,
                implementation_simplicity=3,
                catalyst_timing_specificity=3,
            ),
        ),
        MispricingCandidate(
            name="Candidate B",
            thesis="B",
            underlying="BBB",
            mispricing_type="variance_underpricing",
            posture="long_vol",
            preferred_expression="straddle",
            time_horizon="3-6m",
            mispricing_signals=MispricingSignals(
                hiddenness=4,
                recognition_gap=4,
                catalyst_clarity=2,
                propagation_asymmetry=4,
                duration_mismatch=2,
                evidence_quality=3,
                crowding_inverse=4,
                valuation_nonlinearity=5,
            ),
            options_expression_signals=OptionsExpressionSignals(
                convexity_need=5,
                tenor_alignment=3,
                vol_expansion_potential=4,
                downside_definedness=4,
                liquidity_path=2,
                implementation_simplicity=3,
                catalyst_timing_specificity=2,
            ),
        ),
    ]

    results = screen_candidates(candidates)

    assert [result.candidate_name for result in results] == ["Candidate A", "Candidate B"]
