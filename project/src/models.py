from dataclasses import dataclass, field
from typing import Optional, Dict


# -----------------------------
# Gemini Response
# -----------------------------
@dataclass
class GeminiResponse:
    success: bool
    content: Optional[str]
    usage: Optional[Dict]
    error: Optional[str]


# -----------------------------
# Discovery Result
# -----------------------------
@dataclass
class DiscoveryResult:
    app: str
    official_site: str

    developer_docs: Optional[str] = None
    api_reference: Optional[str] = None
    authentication_docs: Optional[str] = None
    pricing: Optional[str] = None
    webhooks: Optional[str] = None
    openapi: Optional[str] = None
    mcp: Optional[str] = None


# -----------------------------
# Research Result
# -----------------------------
@dataclass
class ResearchResult:

    app: str

    category: Optional[str] = None
    description: Optional[str] = None

    auth_method: Optional[str] = None
    self_serve: Optional[str] = None

    api_type: Optional[str] = None
    api_surface: Optional[str] = None

    buildability: Optional[str] = None
    blocker: Optional[str] = None

    evidence: Dict = field(default_factory=dict)

    confidence: int = 0


# -----------------------------
# Verification Result
# -----------------------------
@dataclass
class VerificationResult:

    app: str

    verified: bool

    confidence: int

    notes: Optional[str] = None