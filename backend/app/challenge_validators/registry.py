from typing import Dict, Optional
from . import Validator


_REGISTRY: Dict[int, Validator] = {}


def register_validator(exercise_id: int, validator: Validator) -> None:
    _REGISTRY[exercise_id] = validator


def get_validator_for_exercise(exercise_id: int) -> Optional[Validator]:
    return _REGISTRY.get(exercise_id)


# Example default validator (no-op)
class NoopValidator:
    def get_public_params(self, user, exercise_id: int):
        return {"version": "1.0.0"}

    def validate(self, submission, user, exercise_id: int, public_params):
        # fall back to default numeric sum correctness (handled outside)
        return True


# Optionally register a few demo validators here
# register_validator(1, NoopValidator())

