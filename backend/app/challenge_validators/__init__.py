from typing import Protocol, Any, Dict


class Validator(Protocol):
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        ...

    def validate(
        self,
        submission: Any,
        user: Any,
        exercise_id: int,
        public_params: Dict[str, Any],
    ) -> bool:
        ...


