"""
Canonical ontology definition for bottleneck-focused research mode.

This is intentionally separate from the social-simulation ontology generator.
It defines the stable entity and relationship vocabulary that future research
projects, API endpoints, and prompt templates should target.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class OntologyAttribute:
    name: str
    description: str
    field_type: str = "text"

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "type": self.field_type,
            "description": self.description,
        }


@dataclass(frozen=True)
class OntologyEntityType:
    name: str
    description: str
    attributes: List[OntologyAttribute] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "attributes": [attribute.to_dict() for attribute in self.attributes],
        }


@dataclass(frozen=True)
class OntologyRelationshipType:
    name: str
    description: str
    source_targets: List[Dict[str, str]]
    attributes: List[OntologyAttribute] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "source_targets": list(self.source_targets),
            "attributes": [attribute.to_dict() for attribute in self.attributes],
        }


@dataclass(frozen=True)
class EvidenceRequirement:
    claim_type: str
    minimum_sources: int
    required_source_classes: List[str]
    notes: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


ONTOLOGY_NAME = "bottleneck_research"
ONTOLOGY_VERSION = "v1"

SUPPORTED_SOURCE_CLASSES: List[str] = [
    "company_filing",
    "company_release",
    "earnings_transcript",
    "government",
    "policy_tracker",
    "industry_body",
    "technical_paper",
    "conference_material",
    "trade_press",
    "analyst_note",
    "investor_post",
    "forum_post",
    "user_note",
    "captured_image",
    "market_data_snapshot",
]

SUPPORTED_CLAIM_TYPES: List[str] = [
    "component_dependency",
    "material_or_processing_dependency",
    "supplier_or_customer_relationship",
    "market_share_or_concentration",
    "capacity_expansion_or_ramp",
    "export_control_or_policy",
    "demand_acceleration",
    "bottleneck_assertion",
    "event_translation",
    "valuation_gap_assertion",
    "expression_fit_assertion",
]


RESEARCH_ENTITY_TYPES: List[OntologyEntityType] = [
    OntologyEntityType(
        name="Theme",
        description="Top-level research theme or bottleneck narrative.",
        attributes=[
            OntologyAttribute("title", "Short research theme title"),
            OntologyAttribute("scope", "Thematic scope and boundaries"),
        ],
    ),
    OntologyEntityType(
        name="MarketDriver",
        description="Demand-side force increasing system stress or adoption.",
        attributes=[
            OntologyAttribute("driver_type", "Demand, policy, regulatory, or technology driver"),
            OntologyAttribute("time_horizon", "Expected time horizon of impact"),
        ],
    ),
    OntologyEntityType(
        name="EndMarket",
        description="Demand destination consuming the system or component.",
        attributes=[
            OntologyAttribute("market_name", "Name of the end market"),
            OntologyAttribute("growth_profile", "Expected growth or adoption profile"),
        ],
    ),
    OntologyEntityType(
        name="System",
        description="Deployed product or infrastructure system being analyzed.",
        attributes=[
            OntologyAttribute("system_name", "Canonical system name"),
            OntologyAttribute("system_scope", "Practical boundary of the system"),
        ],
    ),
    OntologyEntityType(
        name="Subsystem",
        description="Cost or function-critical subsystem within a broader system.",
        attributes=[
            OntologyAttribute("subsystem_name", "Canonical subsystem name"),
            OntologyAttribute("bom_weight", "Relative importance in cost or performance"),
        ],
    ),
    OntologyEntityType(
        name="SystemLayer",
        description="Top-level deployed system or infrastructure layer.",
        attributes=[
            OntologyAttribute("layer_name", "Name of the system layer"),
            OntologyAttribute("functional_role", "Role in the full chain"),
        ],
    ),
    OntologyEntityType(
        name="Component",
        description="Intermediate component, module, or subsystem in the chain.",
        attributes=[
            OntologyAttribute("component_name", "Component or subsystem name"),
            OntologyAttribute("qualification_level", "Qualification or switching difficulty"),
        ],
    ),
    OntologyEntityType(
        name="MaterialInput",
        description="Raw material, substrate, refined input, or specialty consumable.",
        attributes=[
            OntologyAttribute("material_name", "Material or refined input name"),
            OntologyAttribute("processing_stage", "Mining, refining, separation, substrate, or other stage"),
        ],
    ),
    OntologyEntityType(
        name="ProcessLayer",
        description="Processing or refining stage that converts inputs into usable industrial form.",
        attributes=[
            OntologyAttribute("process_name", "Name of the process layer"),
            OntologyAttribute("process_stage", "Refining, separation, deposition, packaging, or assembly"),
        ],
    ),
    OntologyEntityType(
        name="BottleneckLayer",
        description="Specific layer identified as constrained or strategically important.",
        attributes=[
            OntologyAttribute("layer_name", "Human-readable bottleneck layer name"),
            OntologyAttribute("severity_band", "Low, emerging, moderate, high, or critical"),
            OntologyAttribute("value_capture_band", "Low, emerging, moderate, high, or critical"),
        ],
    ),
    OntologyEntityType(
        name="ExpressionCandidate",
        description="Potential public-market expression such as shares, LEAPS, basket, or long-vol setup.",
        attributes=[
            OntologyAttribute("expression_type", "Shares, leaps_call, basket, long_vol, or reject"),
            OntologyAttribute("time_horizon", "Expected holding period or timing window"),
        ],
    ),
    OntologyEntityType(
        name="PublicCompany",
        description="Listed company exposed to the bottleneck theme.",
        attributes=[
            OntologyAttribute("ticker", "Primary ticker or market symbol"),
            OntologyAttribute("exposure_type", "Pure-play, adjacent, diversified, or enabling"),
        ],
    ),
    OntologyEntityType(
        name="Facility",
        description="Physical plant, fab, refinery, line, or manufacturing site.",
        attributes=[
            OntologyAttribute("facility_name", "Facility or project name"),
            OntologyAttribute("capacity_stage", "Operating, ramping, announced, or planned"),
        ],
    ),
    OntologyEntityType(
        name="Geography",
        description="Country, region, or location relevant to concentration or policy risk.",
        attributes=[
            OntologyAttribute("geo_name", "Country or regional name"),
            OntologyAttribute("risk_profile", "Strategic, diversified, constrained, or policy-sensitive"),
        ],
    ),
    OntologyEntityType(
        name="PolicyAction",
        description="Export control, subsidy, standard, or industrial-policy action.",
        attributes=[
            OntologyAttribute("policy_name", "Policy or action name"),
            OntologyAttribute("policy_type", "Export control, subsidy, standard, grant, or regulation"),
        ],
    ),
    OntologyEntityType(
        name="Event",
        description="Discrete event or catalyst that can translate structural stress into market repricing.",
        attributes=[
            OntologyAttribute("event_name", "Name of the event or catalyst"),
            OntologyAttribute("event_type", "Earnings, policy, qualification, ramp, disruption, or media recognition"),
        ],
    ),
    OntologyEntityType(
        name="CapacityExpansion",
        description="Project or investment intended to add qualified supply.",
        attributes=[
            OntologyAttribute("project_name", "Expansion project name"),
            OntologyAttribute("expected_start", "Expected start or ramp date"),
        ],
    ),
    OntologyEntityType(
        name="Claim",
        description="Structured research claim to be audited against sources.",
        attributes=[
            OntologyAttribute("claim_text", "Structured factual or inferential claim"),
            OntologyAttribute("status", "Supported, unverified, or unsupported"),
            OntologyAttribute("confidence", "Low, medium, or high"),
        ],
    ),
    OntologyEntityType(
        name="Source",
        description="Primary or secondary source supporting a claim.",
        attributes=[
            OntologyAttribute("source_url", "Canonical source URL"),
            OntologyAttribute("source_class", "Normalized source class used for ingestion"),
            OntologyAttribute("usage_mode", "Evidence, context, hypothesis_seed, or market_signal"),
        ],
    ),
    OntologyEntityType(
        name="SourceFragment",
        description="Indexed excerpt or fragment extracted from a source.",
        attributes=[
            OntologyAttribute("fragment_id", "Stable source fragment identifier"),
            OntologyAttribute("fragment_type", "Paragraph, quote, screenshot region, or table row"),
            OntologyAttribute("section_label", "Local section or heading label"),
        ],
    ),
    OntologyEntityType(
        name="Inference",
        description="Explicit inferential bridge from evidence to a structural or market conclusion.",
        attributes=[
            OntologyAttribute("inference_type", "Dependency, bottleneck, event translation, or expression inference"),
            OntologyAttribute("confidence", "Low, medium, or high"),
        ],
    ),
]


RESEARCH_RELATIONSHIP_TYPES: List[OntologyRelationshipType] = [
    OntologyRelationshipType(
        name="PART_OF",
        description="A subsystem, component, or layer is part of a broader system.",
        source_targets=[
            {"source": "Subsystem", "target": "System"},
            {"source": "Component", "target": "Subsystem"},
            {"source": "SystemLayer", "target": "System"},
            {"source": "BottleneckLayer", "target": "Subsystem"},
        ],
    ),
    OntologyRelationshipType(
        name="DRIVEN_BY",
        description="Theme or system is driven by a market or policy force.",
        source_targets=[
            {"source": "Theme", "target": "MarketDriver"},
            {"source": "BottleneckLayer", "target": "MarketDriver"},
            {"source": "System", "target": "MarketDriver"},
        ],
    ),
    OntologyRelationshipType(
        name="USED_IN",
        description="Component, material, or bottleneck layer is used in a system or end market.",
        source_targets=[
            {"source": "MaterialInput", "target": "Component"},
            {"source": "Component", "target": "Subsystem"},
            {"source": "Subsystem", "target": "System"},
            {"source": "Component", "target": "SystemLayer"},
            {"source": "SystemLayer", "target": "EndMarket"},
            {"source": "BottleneckLayer", "target": "EndMarket"},
        ],
    ),
    OntologyRelationshipType(
        name="DEPENDS_ON",
        description="A layer or system depends on another layer or input.",
        source_targets=[
            {"source": "SystemLayer", "target": "Component"},
            {"source": "System", "target": "Subsystem"},
            {"source": "Subsystem", "target": "Component"},
            {"source": "Component", "target": "MaterialInput"},
            {"source": "Component", "target": "ProcessLayer"},
            {"source": "ProcessLayer", "target": "MaterialInput"},
            {"source": "BottleneckLayer", "target": "MaterialInput"},
            {"source": "BottleneckLayer", "target": "Component"},
            {"source": "BottleneckLayer", "target": "ProcessLayer"},
            {"source": "BottleneckLayer", "target": "SystemLayer"},
        ],
    ),
    OntologyRelationshipType(
        name="PROCESSED_BY",
        description="A material or component relies on a specific processing layer.",
        source_targets=[
            {"source": "MaterialInput", "target": "ProcessLayer"},
            {"source": "Component", "target": "ProcessLayer"},
            {"source": "BottleneckLayer", "target": "ProcessLayer"},
        ],
    ),
    OntologyRelationshipType(
        name="SUPPLIED_BY",
        description="A bottleneck layer, component, or material is supplied by a public company.",
        source_targets=[
            {"source": "MaterialInput", "target": "PublicCompany"},
            {"source": "ProcessLayer", "target": "PublicCompany"},
            {"source": "Component", "target": "PublicCompany"},
            {"source": "BottleneckLayer", "target": "PublicCompany"},
        ],
    ),
    OntologyRelationshipType(
        name="QUALIFIED_BY",
        description="A component, layer, or supplier is qualified by a customer or ecosystem participant.",
        source_targets=[
            {"source": "Component", "target": "PublicCompany"},
            {"source": "BottleneckLayer", "target": "PublicCompany"},
            {"source": "PublicCompany", "target": "PublicCompany"},
        ],
    ),
    OntologyRelationshipType(
        name="LOCATED_IN",
        description="Facility, company, or layer has important concentration in a geography.",
        source_targets=[
            {"source": "Facility", "target": "Geography"},
            {"source": "PublicCompany", "target": "Geography"},
            {"source": "BottleneckLayer", "target": "Geography"},
        ],
    ),
    OntologyRelationshipType(
        name="CONSTRAINED_BY",
        description="A layer is constrained by policy, qualification, or capacity expansion timing.",
        source_targets=[
            {"source": "BottleneckLayer", "target": "PolicyAction"},
            {"source": "BottleneckLayer", "target": "CapacityExpansion"},
            {"source": "ProcessLayer", "target": "PolicyAction"},
            {"source": "System", "target": "PolicyAction"},
            {"source": "PublicCompany", "target": "PolicyAction"},
        ],
    ),
    OntologyRelationshipType(
        name="AFFECTED_BY_EVENT",
        description="A market-relevant layer or company is affected by a discrete event or catalyst.",
        source_targets=[
            {"source": "Theme", "target": "Event"},
            {"source": "BottleneckLayer", "target": "Event"},
            {"source": "PublicCompany", "target": "Event"},
            {"source": "ExpressionCandidate", "target": "Event"},
        ],
    ),
    OntologyRelationshipType(
        name="EXPANDS_CAPACITY_FOR",
        description="A facility or expansion project adds capacity for a layer or company.",
        source_targets=[
            {"source": "CapacityExpansion", "target": "BottleneckLayer"},
            {"source": "CapacityExpansion", "target": "PublicCompany"},
            {"source": "Facility", "target": "BottleneckLayer"},
        ],
    ),
    OntologyRelationshipType(
        name="SUPPORTS_CLAIM",
        description="A source supports or challenges a research claim.",
        source_targets=[
            {"source": "Source", "target": "Claim"},
        ],
        attributes=[
            OntologyAttribute("support_type", "supporting, contradictory, or contextual"),
        ],
    ),
    OntologyRelationshipType(
        name="EVIDENCED_BY",
        description="A claim or inference is directly evidenced by a specific source fragment.",
        source_targets=[
            {"source": "Claim", "target": "SourceFragment"},
            {"source": "Inference", "target": "SourceFragment"},
        ],
        attributes=[
            OntologyAttribute("evidence_role", "direct, contextual, or contradictory"),
        ],
    ),
    OntologyRelationshipType(
        name="DESCRIBES",
        description="A claim describes a specific theme, layer, company, or policy action.",
        source_targets=[
            {"source": "Claim", "target": "Theme"},
            {"source": "Claim", "target": "System"},
            {"source": "Claim", "target": "Subsystem"},
            {"source": "Claim", "target": "Component"},
            {"source": "Claim", "target": "ProcessLayer"},
            {"source": "Claim", "target": "BottleneckLayer"},
            {"source": "Claim", "target": "PublicCompany"},
            {"source": "Claim", "target": "PolicyAction"},
            {"source": "Claim", "target": "Event"},
            {"source": "Claim", "target": "ExpressionCandidate"},
        ],
    ),
    OntologyRelationshipType(
        name="ALTERNATIVE_TO",
        description="A layer, component, or material competes with or substitutes for another.",
        source_targets=[
            {"source": "Component", "target": "Component"},
            {"source": "MaterialInput", "target": "MaterialInput"},
            {"source": "BottleneckLayer", "target": "BottleneckLayer"},
        ],
    ),
    OntologyRelationshipType(
        name="ANCHORS",
        description="An anchor company or bottleneck layer organizes a research universe.",
        source_targets=[
            {"source": "Theme", "target": "PublicCompany"},
            {"source": "BottleneckLayer", "target": "PublicCompany"},
        ],
    ),
    OntologyRelationshipType(
        name="SATELLITE_TO",
        description="A less-followed company is an asymmetric satellite around a better-known anchor.",
        source_targets=[
            {"source": "PublicCompany", "target": "PublicCompany"},
        ],
    ),
    OntologyRelationshipType(
        name="CANDIDATE_EXPRESSION_FOR",
        description="A proposed expression targets a company or theme.",
        source_targets=[
            {"source": "ExpressionCandidate", "target": "PublicCompany"},
            {"source": "ExpressionCandidate", "target": "Theme"},
            {"source": "ExpressionCandidate", "target": "BottleneckLayer"},
        ],
    ),
    OntologyRelationshipType(
        name="REPRICES_VIA",
        description="An expression is expected to reprice through a catalyst or event path.",
        source_targets=[
            {"source": "ExpressionCandidate", "target": "Event"},
            {"source": "ExpressionCandidate", "target": "PolicyAction"},
            {"source": "ExpressionCandidate", "target": "MarketDriver"},
        ],
    ),
    OntologyRelationshipType(
        name="INFERRED_FROM",
        description="An inference bridges multiple claims or entities into a structural conclusion.",
        source_targets=[
            {"source": "Inference", "target": "Claim"},
            {"source": "Inference", "target": "Theme"},
            {"source": "Inference", "target": "BottleneckLayer"},
            {"source": "Inference", "target": "ExpressionCandidate"},
        ],
    ),
]

RESEARCH_EDGE_TYPES: List[OntologyRelationshipType] = RESEARCH_RELATIONSHIP_TYPES


EVIDENCE_REQUIREMENTS: List[EvidenceRequirement] = [
    EvidenceRequirement(
        claim_type="market_share_or_concentration",
        minimum_sources=1,
        required_source_classes=["company_filing", "government", "industry_body"],
        notes="Prefer filings or government/industry-body data over media summaries.",
    ),
    EvidenceRequirement(
        claim_type="capacity_expansion_or_ramp",
        minimum_sources=1,
        required_source_classes=["company_release", "company_filing", "government"],
        notes="Company releases are acceptable, but filings or government corroboration are preferred when available.",
    ),
    EvidenceRequirement(
        claim_type="export_control_or_policy",
        minimum_sources=1,
        required_source_classes=["government", "policy_tracker", "company_filing"],
        notes="Must be grounded in a policy or government source, or a filing that quotes the policy directly.",
    ),
    EvidenceRequirement(
        claim_type="demand_acceleration",
        minimum_sources=1,
        required_source_classes=["company_filing", "government", "company_release"],
        notes="Use company or government demand statements, but treat pure narrative extrapolation as insufficient.",
    ),
    EvidenceRequirement(
        claim_type="bottleneck_assertion",
        minimum_sources=2,
        required_source_classes=["government", "industry_body", "company_filing"],
        notes="At least one source should describe the constraint directly rather than only implying it.",
    ),
    EvidenceRequirement(
        claim_type="component_dependency",
        minimum_sources=1,
        required_source_classes=["technical_paper", "company_filing", "conference_material"],
        notes="Prefer technical or company materials that explicitly tie the component to the system.",
    ),
    EvidenceRequirement(
        claim_type="material_or_processing_dependency",
        minimum_sources=1,
        required_source_classes=["technical_paper", "government", "company_filing"],
        notes="Use sources that explicitly connect the material or process layer to system performance or cost.",
    ),
    EvidenceRequirement(
        claim_type="supplier_or_customer_relationship",
        minimum_sources=1,
        required_source_classes=["company_release", "earnings_transcript", "company_filing"],
        notes="Supplier/customer edges should be backed by direct company statements whenever possible.",
    ),
    EvidenceRequirement(
        claim_type="event_translation",
        minimum_sources=1,
        required_source_classes=["government", "company_release", "trade_press"],
        notes="Use direct event sources or high-quality reporting that makes the event timing explicit.",
    ),
    EvidenceRequirement(
        claim_type="valuation_gap_assertion",
        minimum_sources=2,
        required_source_classes=["company_filing", "analyst_note", "market_data_snapshot"],
        notes="Requires evidence of valuation mismatch, market misunderstanding, or underfollowed exposure.",
    ),
    EvidenceRequirement(
        claim_type="expression_fit_assertion",
        minimum_sources=2,
        required_source_classes=["market_data_snapshot", "company_filing", "analyst_note"],
        notes="Use chain data plus structural thesis evidence before preferring LEAPS over shares.",
    ),
]


CASE_STUDY_TO_ONTOLOGY_MAPPING: Dict[str, Dict[str, List[str]]] = {
    "thesis-intake": {
        "Theme": ["title", "why this matters"],
        "MarketDriver": ["raw claims", "why it might be mispriced"],
        "EndMarket": ["initial dependency chain"],
        "BottleneckLayer": ["raw claims", "expression candidates"],
    },
    "source-bundle": {
        "Source": ["source_id", "source_class", "usage_mode"],
        "SourceFragment": ["fragment_id", "section_label", "excerpt"],
    },
    "structural-parse": {
        "System": ["canonical_name", "attributes"],
        "Subsystem": ["canonical_name", "attributes"],
        "Component": ["canonical_name", "attributes"],
        "ProcessLayer": ["canonical_name", "attributes"],
        "Claim": ["claim_text", "status", "confidence"],
        "Inference": ["inference_type", "confidence"],
    },
    "claims-audit": {
        "Claim": ["claim_text", "status", "confidence"],
        "Source": ["source_url", "source_type"],
    },
    "chokepoint-scores": {
        "BottleneckLayer": ["severity_signals", "value_capture_signals"],
        "PublicCompany": ["public_companies"],
    },
    "case-study-summary": {
        "Theme": ["objective", "interpretation"],
        "BottleneckLayer": ["scoring output", "follow-up questions"],
        "PolicyAction": ["claims audit and interpretation"],
        "CapacityExpansion": ["claims audit and interpretation"],
    },
}


def build_research_ontology_spec() -> Dict[str, object]:
    """Return the canonical bottleneck-research ontology specification."""
    spec = {
        "ontology_name": ONTOLOGY_NAME,
        "ontology_version": ONTOLOGY_VERSION,
        "entity_types": [entity.to_dict() for entity in RESEARCH_ENTITY_TYPES],
        "edge_types": [relationship.to_dict() for relationship in RESEARCH_EDGE_TYPES],
        "relationship_types": [
            relationship.to_dict() for relationship in RESEARCH_RELATIONSHIP_TYPES
        ],
        "evidence_requirements": [
            requirement.to_dict() for requirement in EVIDENCE_REQUIREMENTS
        ],
        "artifact_mapping": CASE_STUDY_TO_ONTOLOGY_MAPPING,
        "score_dimensions": ["severity", "value_capture"],
        "supported_source_classes": list(SUPPORTED_SOURCE_CLASSES),
        "supported_claim_types": list(SUPPORTED_CLAIM_TYPES),
    }
    validate_research_ontology_spec(spec)
    return spec


def build_research_graph_ontology() -> Dict[str, object]:
    """
    Return the ontology payload compatible with the current graph builder.

    The existing graph stack expects `entity_types` and `edge_types`, while the
    broader research spec also exposes richer metadata.
    """
    spec = build_research_ontology_spec()
    return {
        "ontology_name": spec["ontology_name"],
        "ontology_version": spec["ontology_version"],
        "entity_types": spec["entity_types"],
        "edge_types": spec["edge_types"],
    }


def validate_research_ontology_spec(spec: Dict[str, object]) -> None:
    """Validate the stable research ontology contract."""
    required_keys = {
        "ontology_name",
        "ontology_version",
        "entity_types",
        "edge_types",
        "relationship_types",
        "evidence_requirements",
        "artifact_mapping",
        "score_dimensions",
        "supported_source_classes",
        "supported_claim_types",
    }
    missing = required_keys - set(spec)
    if missing:
        raise ValueError(f"ontology spec missing keys: {sorted(missing)}")

    entity_types = spec["entity_types"]
    edge_types = spec["edge_types"]
    relationship_types = spec["relationship_types"]
    evidence_requirements = spec["evidence_requirements"]
    artifact_mapping = spec["artifact_mapping"]
    score_dimensions = spec["score_dimensions"]
    supported_source_classes = set(spec["supported_source_classes"])
    supported_claim_types = set(spec["supported_claim_types"])

    if not isinstance(entity_types, list) or not entity_types:
        raise ValueError("entity_types must be a non-empty list")
    if not isinstance(edge_types, list) or not edge_types:
        raise ValueError("edge_types must be a non-empty list")
    if not isinstance(relationship_types, list) or not relationship_types:
        raise ValueError("relationship_types must be a non-empty list")
    if edge_types != relationship_types:
        raise ValueError("edge_types and relationship_types must match exactly")
    if list(score_dimensions) != ["severity", "value_capture"]:
        raise ValueError("score_dimensions must be ['severity', 'value_capture']")

    entity_names = [entity["name"] for entity in entity_types]
    relationship_names = [relationship["name"] for relationship in relationship_types]

    if len(entity_names) != len(set(entity_names)):
        raise ValueError("entity type names must be unique")
    if len(relationship_names) != len(set(relationship_names)):
        raise ValueError("relationship type names must be unique")

    required_entity_names = {
        "Theme",
        "BottleneckLayer",
        "PublicCompany",
        "Claim",
        "Source",
    }
    required_relationship_names = {
        "DEPENDS_ON",
        "SUPPLIED_BY",
        "SUPPORTS_CLAIM",
        "DESCRIBES",
    }

    if not required_entity_names.issubset(set(entity_names)):
        raise ValueError("required entity types are missing from ontology")
    if not required_relationship_names.issubset(set(relationship_names)):
        raise ValueError("required relationship types are missing from ontology")

    expected_artifacts = {
        "thesis-intake",
        "source-bundle",
        "structural-parse",
        "claims-audit",
        "chokepoint-scores",
        "case-study-summary",
    }
    if set(artifact_mapping) != expected_artifacts:
        raise ValueError("artifact_mapping must cover the canonical case-study files")

    for entity in entity_types:
        for attribute in entity.get("attributes", []):
            if "type" not in attribute:
                raise ValueError("entity attribute definitions must include `type`")

    for relationship in relationship_types:
        if not relationship.get("source_targets"):
            raise ValueError("every relationship type must declare source_targets")
        for attribute in relationship.get("attributes", []):
            if "type" not in attribute:
                raise ValueError("relationship attribute definitions must include `type`")

    for requirement in evidence_requirements:
        claim_type = requirement["claim_type"]
        source_classes = set(requirement["required_source_classes"])

        if claim_type not in supported_claim_types:
            raise ValueError(f"unsupported evidence claim_type: {claim_type}")
        if not source_classes:
            raise ValueError("evidence requirements must declare source classes")
        if not source_classes.issubset(supported_source_classes):
            raise ValueError(
                f"unsupported source class in evidence requirement: {claim_type}"
            )
