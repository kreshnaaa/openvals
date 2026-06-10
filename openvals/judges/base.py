from abc import ABC
from abc import abstractmethod


class BaseJudge(ABC):

    """
    Base interface for all OpenVals judges.

    Every judge implementation must return
    a JudgeVerdict object.
    """

    @abstractmethod
    def evaluate(
        self,
        prompt,
        output,
        expected=None,
        context=None,
        metadata=None
    ):

        """
        Evaluate a model output.

        Args:
            prompt: Original user/task prompt.
            output: Model-generated response.
            expected: Optional expected answer.
            context: Optional grounding/context data.
            metadata: Optional extra evaluation metadata.

        Returns:
            JudgeVerdict
        """

        raise NotImplementedError