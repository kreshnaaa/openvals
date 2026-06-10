from dataclasses import dataclass
from typing import List

@dataclass
class JudgeVerdict:

    verdict: str

    confidence: float

    reason: str

    evidence: List[str]

    judge: str