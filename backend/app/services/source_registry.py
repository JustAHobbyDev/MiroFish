"""
Source registry builder for structural information arbitrage.

The source registry is not evidence. It is an acquisition-layer artifact that
tracks which source venues should be monitored or ingested for a thesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_DOCS_DIR = Path(__file__).resolve().parents[3] / "docs" / "research-frameworks"
DEFAULT_MATRIX_PATH = DEFAULT_DOCS_DIR / "2026-03-16-source-priority-matrix-v1.md"
DEFAULT_INVESTIGATION_PATH = DEFAULT_DOCS_DIR / "2026-03-16-source-investigation-list-v1.md"
REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class SourceClassProfile:
    source_class: str
    suggested_ingestion_class: str
    role: str
    priority_tier: str
    authority_score_1_to_5: int
    lead_time_score_1_to_5: int
    graph_centrality_score_1_to_5: int
    market_impact_score_1_to_5: int
    parse_utility_score_1_to_5: int
    ingestion_cadence: str
    access_mode: str
    requires_login: bool
    expected_artifact_types: List[str]
    parser_focus: List[str]
    target_domains: List[str]

    @property
    def priority_score_0_to_100(self) -> float:
        total = (
            self.authority_score_1_to_5
            + self.lead_time_score_1_to_5
            + self.graph_centrality_score_1_to_5
            + self.market_impact_score_1_to_5
            + self.parse_utility_score_1_to_5
        )
        return round((total / 25.0) * 100.0, 2)


CLASS_PROFILES: Dict[str, SourceClassProfile] = {
    "government_policy_enforcement": SourceClassProfile(
        source_class="government_policy_enforcement",
        suggested_ingestion_class="government",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=5,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=5,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="event-driven + weekly sweep",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["policy_notice", "enforcement_notice", "rule_update"],
        parser_focus=["PolicyAction", "Geography", "MaterialInput", "ProcessLayer", "AFFECTED_BY_EVENT", "CONSTRAINED_BY"],
        target_domains=["semiconductors", "ai_infrastructure", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "government_industrial_base_award": SourceClassProfile(
        source_class="government_industrial_base_award",
        suggested_ingestion_class="government",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=5,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=5,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="event-driven + weekly sweep",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["award_notice", "grant_announcement", "contract_notice"],
        parser_focus=["Event", "Facility", "ProcessLayer", "PublicCompany", "EXPANDS_CAPACITY_FOR", "AFFECTED_BY_EVENT"],
        target_domains=["semiconductors", "ai_infrastructure", "critical_materials", "energy_infrastructure", "robotics", "defense"],
    ),
    "company_filing": SourceClassProfile(
        source_class="company_filing",
        suggested_ingestion_class="company_filing",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=5,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="filing-driven + daily watchlist monitoring",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["filing", "annual_report", "quarterly_report", "material_event"],
        parser_focus=["PublicCompany", "Facility", "ProcessLayer", "MaterialInput", "SUPPLIED_BY", "DEPENDS_ON", "CANDIDATE_EXPRESSION_FOR"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "earnings_transcript": SourceClassProfile(
        source_class="earnings_transcript",
        suggested_ingestion_class="earnings_transcript",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="earnings-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["transcript", "prepared_remarks", "qa_transcript"],
        parser_focus=["PublicCompany", "Customer", "ProcessLayer", "Event", "REPRICES_VIA"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "industry_body_and_standards": SourceClassProfile(
        source_class="industry_body_and_standards",
        suggested_ingestion_class="industry_body",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=5,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=5,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="monthly + event-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["industry_report", "standard", "roadmap", "commentary"],
        parser_focus=["System", "Subsystem", "Component", "MaterialInput", "ProcessLayer", "USED_IN", "DEPENDS_ON"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "energy_infrastructure", "robotics", "critical_materials"],
    ),
    "supplier_customer_disclosure": SourceClassProfile(
        source_class="supplier_customer_disclosure",
        suggested_ingestion_class="company_release",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="daily / event-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["partnership_release", "qualification_update", "production_readiness"],
        parser_focus=["PublicCompany", "ProcessLayer", "QUALIFIED_BY", "SUPPLIED_BY", "EXPANDS_CAPACITY_FOR"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "robotics"],
    ),
    "foreign_exchange_filing": SourceClassProfile(
        source_class="foreign_exchange_filing",
        suggested_ingestion_class="company_filing",
        role="graph_forming",
        priority_tier="P0",
        authority_score_1_to_5=5,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="daily for tracked names",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["exchange_filing", "issuer_disclosure", "market_notice"],
        parser_focus=["PublicCompany", "Facility", "ProcessLayer", "MaterialInput", "Event"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "critical_materials", "robotics"],
    ),
    "technical_conference_material": SourceClassProfile(
        source_class="technical_conference_material",
        suggested_ingestion_class="conference_material",
        role="graph_forming",
        priority_tier="P1",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=5,
        ingestion_cadence="conference cycle + event-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["conference_slide", "talk_abstract", "ecosystem_demo"],
        parser_focus=["System", "Subsystem", "Component", "ProcessLayer", "USED_IN", "DEPENDS_ON"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "robotics"],
    ),
    "company_release": SourceClassProfile(
        source_class="company_release",
        suggested_ingestion_class="company_release",
        role="graph_forming",
        priority_tier="P1",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="event-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["press_release", "product_release", "investor_update"],
        parser_focus=["PublicCompany", "Event", "ProcessLayer", "CANDIDATE_EXPRESSION_FOR"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "policy_tracker": SourceClassProfile(
        source_class="policy_tracker",
        suggested_ingestion_class="policy_tracker",
        role="graph_confirming",
        priority_tier="P1",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=5,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="weekly scan",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["policy_tracker_entry", "program_status", "rule_summary"],
        parser_focus=["PolicyAction", "Event", "Geography"],
        target_domains=["semiconductors", "ai_infrastructure", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "trade_press_specialist": SourceClassProfile(
        source_class="trade_press_specialist",
        suggested_ingestion_class="trade_press",
        role="graph_confirming",
        priority_tier="P1",
        authority_score_1_to_5=3,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="daily scan",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["trade_article", "industry_analysis", "specialist_summary"],
        parser_focus=["Context", "DependencyBridge", "MarketSignal"],
        target_domains=["semiconductors", "ai_infrastructure", "photonics", "energy_infrastructure", "robotics", "critical_materials"],
    ),
    "market_data_snapshot": SourceClassProfile(
        source_class="market_data_snapshot",
        suggested_ingestion_class="market_data_snapshot",
        role="graph_confirming",
        priority_tier="P1",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=5,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="daily or multi-weekly for watchlist names",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["price_snapshot", "options_chain", "liquidity_check"],
        parser_focus=["ExpressionCandidate", "REPRICES_VIA", "implementation_viability"],
        target_domains=["equities", "options", "ai_infrastructure", "photonics", "critical_materials", "robotics"],
    ),
    "procurement_capex_guidance": SourceClassProfile(
        source_class="procurement_capex_guidance",
        suggested_ingestion_class="government",
        role="graph_forming",
        priority_tier="P1",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="event-driven + weekly sweep",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["procurement_notice", "capex_guidance", "expansion_plan"],
        parser_focus=["Event", "Facility", "EXPANDS_CAPACITY_FOR"],
        target_domains=["energy_infrastructure", "defense", "ai_infrastructure", "robotics"],
    ),
    "patent_filing": SourceClassProfile(
        source_class="patent_filing",
        suggested_ingestion_class="technical_paper",
        role="graph_confirming",
        priority_tier="P2",
        authority_score_1_to_5=3,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=3,
        parse_utility_score_1_to_5=4,
        ingestion_cadence="monthly + thesis-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["patent", "patent_application"],
        parser_focus=["Component", "MaterialInput", "ProcessLayer", "technical_direction"],
        target_domains=["semiconductors", "photonics", "robotics", "energy_infrastructure"],
    ),
    "shipping_trade_flow_data": SourceClassProfile(
        source_class="shipping_trade_flow_data",
        suggested_ingestion_class="market_data_snapshot",
        role="graph_confirming",
        priority_tier="P2",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=4,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=3,
        ingestion_cadence="monthly + thesis-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["trade_table", "flow_snapshot", "customs_dataset"],
        parser_focus=["Geography", "MaterialInput", "flow_validation"],
        target_domains=["critical_materials", "semiconductors", "energy_infrastructure", "robotics"],
    ),
    "job_posting_hiring_signal": SourceClassProfile(
        source_class="job_posting_hiring_signal",
        suggested_ingestion_class="user_note",
        role="graph_suggesting",
        priority_tier="P2",
        authority_score_1_to_5=2,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=3,
        parse_utility_score_1_to_5=3,
        ingestion_cadence="weekly scan",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["job_posting", "hiring_snapshot"],
        parser_focus=["capacity_hint", "facility_hint", "manufacturing_hint"],
        target_domains=["semiconductors", "photonics", "energy_infrastructure", "robotics"],
    ),
    "analyst_note_excerpt": SourceClassProfile(
        source_class="analyst_note_excerpt",
        suggested_ingestion_class="analyst_note",
        role="graph_confirming",
        priority_tier="P2",
        authority_score_1_to_5=3,
        lead_time_score_1_to_5=3,
        graph_centrality_score_1_to_5=2,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=3,
        ingestion_cadence="thesis-driven",
        access_mode="manual",
        requires_login=True,
        expected_artifact_types=["analyst_excerpt", "target_change", "note_summary"],
        parser_focus=["market_consensus", "valuation_context"],
        target_domains=["equities", "options", "ai_infrastructure", "photonics", "robotics", "critical_materials"],
    ),
    "investor_post_high_signal": SourceClassProfile(
        source_class="investor_post_high_signal",
        suggested_ingestion_class="investor_post",
        role="graph_suggesting",
        priority_tier="P2",
        authority_score_1_to_5=2,
        lead_time_score_1_to_5=5,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=3,
        parse_utility_score_1_to_5=2,
        ingestion_cadence="daily scan",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["post", "thread", "idea_fragment"],
        parser_focus=["hypothesis_seed", "theme_discovery", "recognition_dynamics"],
        target_domains=["ai_infrastructure", "photonics", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "forum_post_comment": SourceClassProfile(
        source_class="forum_post_comment",
        suggested_ingestion_class="forum_post",
        role="graph_suggesting",
        priority_tier="P3",
        authority_score_1_to_5=1,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=2,
        market_impact_score_1_to_5=2,
        parse_utility_score_1_to_5=1,
        ingestion_cadence="opportunistic",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["forum_post", "comment_thread"],
        parser_focus=["hypothesis_seed"],
        target_domains=["ai_infrastructure", "photonics", "critical_materials", "robotics"],
    ),
    "generic_news_roundup": SourceClassProfile(
        source_class="generic_news_roundup",
        suggested_ingestion_class="trade_press",
        role="graph_confirming",
        priority_tier="P3",
        authority_score_1_to_5=2,
        lead_time_score_1_to_5=2,
        graph_centrality_score_1_to_5=2,
        market_impact_score_1_to_5=3,
        parse_utility_score_1_to_5=2,
        ingestion_cadence="backlog only",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["news_roundup"],
        parser_focus=["context_only"],
        target_domains=["ai_infrastructure", "photonics", "critical_materials", "energy_infrastructure", "robotics"],
    ),
    "credit_debt_financing": SourceClassProfile(
        source_class="credit_debt_financing",
        suggested_ingestion_class="company_filing",
        role="graph_confirming",
        priority_tier="P2",
        authority_score_1_to_5=4,
        lead_time_score_1_to_5=4,
        graph_centrality_score_1_to_5=3,
        market_impact_score_1_to_5=4,
        parse_utility_score_1_to_5=3,
        ingestion_cadence="event-driven",
        access_mode="web_public",
        requires_login=False,
        expected_artifact_types=["debt_filing", "rating_note", "prospectus"],
        parser_focus=["balance_sheet", "survivability", "dilution_risk"],
        target_domains=["equities", "ai_infrastructure", "photonics", "critical_materials", "robotics"],
    ),
}


CATEGORY_TO_PROFILE: List[tuple[str, str]] = [
    ("Government policy and enforcement sources", "government_policy_enforcement"),
    ("Primary company filings and official disclosures", "company_filing"),
    ("Industry bodies and standards", "industry_body_and_standards"),
    ("Procurement, grant, subsidy, and industrial-base award sources", "government_industrial_base_award"),
    ("Supplier / customer relationship disclosures", "supplier_customer_disclosure"),
    ("Technical conference materials", "technical_conference_material"),
    ("Authoritative trade press and specialist publications", "trade_press_specialist"),
    ("Exchange and listing disclosures outside the U.S.", "foreign_exchange_filing"),
    ("Patent filings", "patent_filing"),
    ("Job postings and hiring plans", "job_posting_hiring_signal"),
    ("Import / export / customs / shipping data", "shipping_trade_flow_data"),
    ("Credit, debt, and financing documents", "credit_debt_financing"),
]


NAME_OVERRIDE_PROFILES: List[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bearnings call transcripts?\b", re.IGNORECASE), "earnings_transcript"),
    (re.compile(r"\bdebt refinancing\b|\bshelf registrations?\b", re.IGNORECASE), "credit_debt_financing"),
    (re.compile(r"\binvestor presentations?\b|\bpress releases?\b", re.IGNORECASE), "company_release"),
    (re.compile(r"\bfederal register\b", re.IGNORECASE), "government_policy_enforcement"),
    (re.compile(r"\bpolicy trackers?\b", re.IGNORECASE), "policy_tracker"),
    (re.compile(r"\bstate incentive announcements?\b", re.IGNORECASE), "procurement_capex_guidance"),
    (re.compile(r"\bprocurement framework announcements?\b|\bfedbizopps\b", re.IGNORECASE), "procurement_capex_guidance"),
    (re.compile(r"\bpartnership announcements?\b|\bqualification updates?\b|\bvolume production readiness\b", re.IGNORECASE), "supplier_customer_disclosure"),
    (re.compile(r"\banalyst note excerpts?\b", re.IGNORECASE), "analyst_note_excerpt"),
]


def _slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return value.strip("_") or "unknown"


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_markdown_source_list(path: Path) -> List[Dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    current_tier = ""
    current_category = ""
    items: List[Dict[str, Any]] = []
    current_item: Optional[Dict[str, Any]] = None

    def flush_current() -> None:
        nonlocal current_item
        if current_item:
            items.append(current_item)
            current_item = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("## "):
            flush_current()
            current_tier = stripped[3:].strip()
            continue
        if stripped.startswith("### "):
            flush_current()
            current_category = stripped[4:].strip()
            continue

        if not current_tier.startswith("Tier "):
            continue

        bullet_match = re.match(r"- `([^`]+)`", stripped)
        if bullet_match:
            flush_current()
            current_item = {
                "name": bullet_match.group(1).strip(),
                "tier_section": current_tier,
                "category": current_category,
                "canonical_url": None,
                "notes": [],
            }
            continue

        if current_item and stripped.startswith("- Website: <") and stripped.endswith(">"):
            current_item["canonical_url"] = stripped[len("- Website: <"):-1]
            continue

        if current_item and stripped.startswith("- "):
            current_item["notes"].append(stripped[2:].strip())

    flush_current()
    return items


def _resolve_profile_key(name: str, category: str) -> str:
    for pattern, profile_key in NAME_OVERRIDE_PROFILES:
        if pattern.search(name):
            return profile_key
    for category_prefix, profile_key in CATEGORY_TO_PROFILE:
        if category.startswith(category_prefix):
            return profile_key
    return "generic_news_roundup"


def _infer_jurisdiction(name: str, url: str | None) -> str:
    name_upper = name.upper()
    if "U.S." in name or "SEC" in name_upper or "FEDERAL" in name_upper or "BIS" in name_upper:
        return "US"
    if "TSX" in name_upper:
        return "CA"
    if "ASX" in name_upper:
        return "AU"
    if "KRX" in name_upper:
        return "KR"
    if "TSE" in name_upper or "JPX" in name_upper:
        return "JP"
    if "TWSE" in name_upper:
        return "TW"
    if "SSE" in name_upper:
        return "CN"
    if "OMX" in name_upper or "NORDIC" in name_upper:
        return "EU"
    if url and ".gov" in url:
        return "US"
    return "global"


def _infer_requires_login(name: str, url: str | None, profile: SourceClassProfile) -> bool:
    if profile.requires_login:
        return True
    lowered = name.lower()
    return "linkedin" in lowered or "subscription" in lowered


def _infer_access_mode(name: str, url: str | None, profile: SourceClassProfile) -> str:
    lowered = name.lower()
    if "linkedin" in lowered:
        return "login_required"
    if "subscription" in " ".join([name] + ([url] if url else [])).lower():
        return "subscription"
    return profile.access_mode


def _infer_target_themes(profile: SourceClassProfile, category: str, name: str) -> List[str]:
    themes = set(profile.target_domains)
    lowered = f"{category} {name}".lower()
    if "photonic" in lowered or "ofc" in lowered or "spie" in lowered:
        themes.update(["photonics", "ai_optics"])
    if "grid" in lowered or "energy" in lowered or "transformer" in lowered or "nema" in lowered:
        themes.update(["energy_infrastructure", "grid_equipment"])
    if "rare earth" in lowered or "materials" in lowered or "trade" in lowered:
        themes.update(["critical_materials", "rare_earths"])
    if "robot" in lowered:
        themes.update(["robotics"])
    if "semi" in lowered or "jedec" in lowered or "sai" in lowered or "semi" in lowered:
        themes.update(["semiconductors"])
    return sorted(themes)


def _infer_expected_artifact_types(profile: SourceClassProfile, name: str) -> List[str]:
    if name.lower() == "earnings call transcripts":
        return ["transcript", "qa_transcript"]
    if name.lower() == "investor presentations and press releases":
        return ["investor_presentation", "press_release"]
    return profile.expected_artifact_types


def build_source_registry_from_docs(
    investigation_path: Path | None = None,
    matrix_path: Path | None = None,
) -> Dict[str, Any]:
    investigation_path = investigation_path or DEFAULT_INVESTIGATION_PATH
    matrix_path = matrix_path or DEFAULT_MATRIX_PATH

    if not investigation_path.exists():
        raise FileNotFoundError(f"source investigation list not found: {investigation_path}")
    if not matrix_path.exists():
        raise FileNotFoundError(f"source priority matrix not found: {matrix_path}")

    items = _parse_markdown_source_list(investigation_path)
    rows: List[Dict[str, Any]] = []

    for item in items:
        profile_key = _resolve_profile_key(item["name"], item["category"])
        profile = CLASS_PROFILES[profile_key]
        url = item.get("canonical_url")
        row = {
            "source_target_id": f"src_target_{_slugify(item['name'])}",
            "name": item["name"],
            "source_family": profile_key,
            "source_class": profile.source_class,
            "suggested_ingestion_class": profile.suggested_ingestion_class,
            "canonical_url": url,
            "role": profile.role,
            "priority_tier": profile.priority_tier,
            "priority_score_0_to_100": profile.priority_score_0_to_100,
            "authority_score_1_to_5": profile.authority_score_1_to_5,
            "lead_time_score_1_to_5": profile.lead_time_score_1_to_5,
            "graph_centrality_score_1_to_5": profile.graph_centrality_score_1_to_5,
            "market_impact_score_1_to_5": profile.market_impact_score_1_to_5,
            "parse_utility_score_1_to_5": profile.parse_utility_score_1_to_5,
            "jurisdiction": _infer_jurisdiction(item["name"], url),
            "category": item["category"],
            "tier_section": item["tier_section"],
            "target_domains": profile.target_domains,
            "target_themes": _infer_target_themes(profile, item["category"], item["name"]),
            "target_systems": [],
            "ingestion_cadence": profile.ingestion_cadence,
            "access_mode": _infer_access_mode(item["name"], url, profile),
            "requires_login": _infer_requires_login(item["name"], url, profile),
            "expected_artifact_types": _infer_expected_artifact_types(profile, item["name"]),
            "parser_focus": profile.parser_focus,
            "status": "candidate",
            "notes": item.get("notes", []),
            "source_doc_refs": [
                _display_path(investigation_path),
                _display_path(matrix_path),
            ],
        }
        rows.append(row)

    rows.sort(
        key=lambda row: (
            -float(row["priority_score_0_to_100"]),
            row["priority_tier"],
            row["name"].lower(),
        )
    )

    return {
        "registry_version": "v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_from": [
            _display_path(investigation_path),
            _display_path(matrix_path),
        ],
        "row_count": len(rows),
        "rows": rows,
    }


__all__ = [
    "DEFAULT_DOCS_DIR",
    "DEFAULT_MATRIX_PATH",
    "DEFAULT_INVESTIGATION_PATH",
    "build_source_registry_from_docs",
]
