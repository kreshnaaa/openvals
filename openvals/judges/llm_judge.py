from openvals.judges.base import BaseJudge
from openvals.judges.verdict import JudgeVerdict


class LLMJudge(BaseJudge):

    def evaluate(
        self,
        prompt,
        output,
        expected=None
    ):

        return JudgeVerdict(

            verdict="NOT_IMPLEMENTED",

            confidence=0.0,

            reason="Judge layer foundation only",

            evidence=[],

            judge="OpenValsJudge"

        )