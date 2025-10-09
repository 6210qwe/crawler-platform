from typing import Dict, Optional
from . import Validator
from .exercises.exercise_1 import Exercise1Validator
from .exercises.exercise_2 import Exercise2Validator
from .exercises.exercise_3 import Exercise3Validator


_REGISTRY: Dict[int, Validator] = {}


def register_validator(exercise_id: int, validator: Validator) -> None:
    _REGISTRY[exercise_id] = validator


def get_validator_for_exercise(exercise_id: int) -> Optional[Validator]:
    return _REGISTRY.get(exercise_id)


def auto_register_validators():
    """自动注册所有验证器"""
    # 注册题目验证器
    register_validator(1, Exercise1Validator())
    register_validator(2, Exercise2Validator())
    register_validator(3, Exercise3Validator())
    
    # 可以在这里添加更多验证器
    # register_validator(4, Exercise4Validator())
    # register_validator(5, Exercise5Validator())


# Example default validator (no-op)
class NoopValidator:
    def get_public_params(self, user, exercise_id: int):
        return {"version": "1.0.0"}

    def validate(self, submission, user, exercise_id: int, public_params):
        # fall back to default numeric sum correctness (handled outside)
        return True


# 自动注册验证器
auto_register_validators()

