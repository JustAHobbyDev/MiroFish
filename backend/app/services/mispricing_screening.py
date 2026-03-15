"""
Mispricing screening utilities for bottleneck and dependency-driven research.

This layer sits downstream of structural thesis work. It does not ingest live
options chains or price volatility surfaces; instead it produces a structured
screen for whether a thesis looks like a plausible options-mispricing candidate
and whether options are a sensible expression path.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Tuple

from .chokepoint_scoring import classify_score, validate_weights


DEFAULT_MISPRICING_WEIGHTS: Dict[str, float] = {
    "hiddenness": 0.18,
    "recognition_gap": 0.18,
    "catalyst_clarity": 0.16,
    "propagation_asymmetry": 0.14,
    "duration_mismatch": 0.12,
    "evidence_quality": 0.10,
    "crowding_inverse": 0.06,
    "valuation_nonlinearity": 0.06,
}

DEFAULT_OPTIONS_FIT_WEIGHTS: Dict[str, float] = {
    "convexity_need": 0.18,
    "tenor_alignment": 0.18,
    "vol_expansion_potential": 0.18,
    "downside_definedness": 0.14,
    "liquidity_path": 0.12,
    "implementation_simplicity": 0.10,
    "catalyst_timing_specificity": 0.10,
}


def _clamp_signal(value: float) -> float:
    return max(0.0, min(5.0, float(value)))


@dataclass
class MispricingSignals:
    """
    Signals for whether a dependency thesis looks underpriced.

    Each field is scored 0-5:
    0 = weak / absent
    5 = strong / highly material
    """

    hiddenness: float
    recognition_gap: float
    catalyst_clarity: float
    propagation_asymmetry: float
    duration_mismatch: float
    evidence_quality: float
    crowding_inverse: float = 0.0
    valuation_nonlinearity: float = 0.0

    def normalized(self) -> Dict[str, float]:
        return {
            key: _clamp_signal(value)
            for key, value in asdict(self).items()
        }


@dataclass
class OptionsExpressionSignals:
    """
    Signals for whether options are a good expression path.

    This is not live market pricing. It is a structural proxy screen for
    convexity fit and potential volatility repricing.
    """

    convexity_need: float
    tenor_alignment: float
    vol_expansion_potential: float
    downside_definedness: float
    liquidity_path: float
    implementation_simplicity: float
    catalyst_timing_specificity: float

    def normalized(self) -> Dict[str, float]:
        return {
            key: _clamp_signal(value)
            for key, value in asdict(self).items()
        }


@dataclass
class MispricingCandidate:
    """Structured mispricing candidate emitted by research workflows."""

    name: str
    thesis: str
    underlying: str
    mispricing_type: str
    posture: str
    preferred_expression: str
    time_horizon: str
    mispricing_signals: MispricingSignals
    options_expression_signals: OptionsExpressionSignals
    linked_companies: List[str] = field(default_factory=list)
    catalysts: List[str] = field(default_factory=list)
    invalidations: List[str] = field(default_factory=list)
    structural_reference: Dict[str, object] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "thesis": self.thesis,
            "underlying": self.underlying,
            "mispricing_type": self.mispricing_type,
            "posture": self.posture,
            "preferred_expression": self.preferred_expression,
            "time_horizon": self.time_horizon,
            "mispricing_signals": self.mispricing_signals.normalized(),
            "options_expression_signals": self.options_expression_signals.normalized(),
            "linked_companies": list(self.linked_companies),
            "catalysts": list(self.catalysts),
            "invalidations": list(self.invalidations),
            "structural_reference": dict(self.structural_reference),
            "notes": list(self.notes),
        }


@dataclass
class MispricingScoreBreakdown:
    """Single score breakdown for mispricing screening."""

    candidate_name: str
    score_type: str
    score_0_to_100: float
    band: str
    weighted_signals: Dict[str, float]
    strongest_drivers: List[Tuple[str, float]]
    weakest_drivers: List[Tuple[str, float]]
    explanation: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "candidate_name": self.candidate_name,
            "score_type": self.score_type,
            "score_0_to_100": round(self.score_0_to_100, 2),
            "band": self.band,
            "weighted_signals": {
                key: round(value, 4) for key, value in self.weighted_signals.items()
            },
            "strongest_drivers": [
                (key, round(value, 4)) for key, value in self.strongest_drivers
            ],
            "weakest_drivers": [
                (key, round(value, 4)) for key, value in self.weakest_drivers
            ],
            "explanation": self.explanation,
        }


@dataclass
class MispricingScorecard:
    """Full scorecard for a mispricing candidate."""

    candidate_name: str
    mispricing: MispricingScoreBreakdown
    options_fit: MispricingScoreBreakdown

    def to_dict(self) -> Dict[str, object]:
        return {
            "candidate_name": self.candidate_name,
            "mispricing": self.mispricing.to_dict(),
            "options_fit": self.options_fit.to_dict(),
        }


def score_mispricing_candidate(
    candidate: MispricingCandidate,
    mispricing_weights: Dict[str, float] | None = None,
    options_fit_weights: Dict[str, float] | None = None,
) -> MispricingScorecard:
    """Score both the thesis mispricing and options-expression fit."""
    return MispricingScorecard(
        candidate_name=candidate.name,
        mispricing=_score_breakdown(
            candidate=candidate,
            score_type="mispricing",
            signals=candidate.mispricing_signals.normalized(),
            weights=mispricing_weights or DEFAULT_MISPRICING_WEIGHTS,
        ),
        options_fit=_score_breakdown(
            candidate=candidate,
            score_type="options_fit",
            signals=candidate.options_expression_signals.normalized(),
            weights=options_fit_weights or DEFAULT_OPTIONS_FIT_WEIGHTS,
        ),
    )


def screen_candidates(
    candidates: List[MispricingCandidate],
    mispricing_weights: Dict[str, float] | None = None,
    options_fit_weights: Dict[str, float] | None = None,
) -> List[MispricingScorecard]:
    """Screen a list of candidates."""
    return [
        score_mispricing_candidate(
            candidate,
            mispricing_weights=mispricing_weights,
            options_fit_weights=options_fit_weights,
        )
        for candidate in candidates
    ]


def _score_breakdown(
    candidate: MispricingCandidate,
    score_type: str,
    signals: Dict[str, float],
    weights: Dict[str, float],
) -> MispricingScoreBreakdown:
    normalized_weights = validate_weights(weights)

    missing = set(normalized_weights) - set(signals)
    if missing:
        raise ValueError(f"missing signals for weights: {sorted(missing)}")

    weighted_signals = {
        key: signals[key] * normalized_weights[key]
        for key in normalized_weights
    }
    weighted_total = sum(weighted_signals.values())
    score_0_to_100 = (weighted_total / 5.0) * 100.0
    band = classify_score(score_0_to_100)

    ordered = sorted(
        weighted_signals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    strongest = ordered[:3]
    weakest = list(reversed(ordered[-2:]))

    return MispricingScoreBreakdown(
        candidate_name=candidate.name,
        score_type=score_type,
        score_0_to_100=score_0_to_100,
        band=band,
        weighted_signals=weighted_signals,
        strongest_drivers=strongest,
        weakest_drivers=weakest,
        explanation=_build_explanation(
            candidate=candidate,
            score_type=score_type,
            score_0_to_100=score_0_to_100,
            band=band,
            strongest=strongest,
            weakest=weakest,
        ),
    )


def _pretty_signal_name(signal_name: str) -> str:
    return signal_name.replace("_", " ")


def _build_explanation(
    candidate: MispricingCandidate,
    score_type: str,
    score_0_to_100: float,
    band: str,
    strongest: List[Tuple[str, float]],
    weakest: List[Tuple[str, float]],
) -> str:
    strongest_text = ", ".join(_pretty_signal_name(name) for name, _ in strongest)
    weakest_text = ", ".join(_pretty_signal_name(name) for name, _ in weakest)

    if score_type == "mispricing":
        return (
            f"{candidate.name} scores {score_0_to_100:.1f}/100 ({band}) on "
            f"mispricing plausibility. The strongest weighted drivers are "
            f"{strongest_text}. The least supportive signals are {weakest_text}. "
            f"This screen is a structural ranking aid, not live options pricing."
        )

    return (
        f"{candidate.name} scores {score_0_to_100:.1f}/100 ({band}) on "
        f"options-expression fit. The strongest weighted drivers are "
        f"{strongest_text}. The least supportive signals are {weakest_text}. "
        f"This screen helps decide whether options are a sensible expression path."
    )
