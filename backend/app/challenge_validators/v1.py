import hashlib
import time
from typing import Any, Dict
from . import Validator


class FirstExerciseValidator:
    """第一题（sort_order=1）：MD5 加密翻页参数校验器"""
    
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        return {
            "timestamp": timestamp,
            "hint": "翻页时需要携带 MD5(timestamp + 'spider') 参数"
        }
    
    def validate(self, submission: Any, user: Any, exercise_id: int, public_params: Dict[str, Any]) -> bool:
        """校验提交的 MD5 参数"""
        try:
            # 获取提交的参数
            payload = getattr(submission, 'payload', {})
            if not payload:
                return False
            
            # 检查必要字段
            if 'timestamp' not in payload or 'md5Param' not in payload:
                return False
            
            submitted_timestamp = payload['timestamp']
            submitted_md5 = payload['md5Param']
            
            # 验证时间戳是否在合理范围内（5分钟内）
            current_time = int(time.time())
            if abs(current_time - submitted_timestamp) > 300:  # 5分钟
                return False
            
            # 生成正确的 MD5
            raw_string = str(submitted_timestamp) + 'spider'
            expected_md5 = hashlib.md5(raw_string.encode('utf-8')).hexdigest()
            
            # 比较 MD5
            if submitted_md5 != expected_md5:
                return False
            
            # 验证答案是否正确（这里可以添加额外的业务逻辑）
            # 例如：检查答案是否在合理范围内
            answer = getattr(submission, 'answer', 0)
            if not isinstance(answer, int) or answer < 0:
                return False
            
            return True
            
        except Exception as e:
            print(f"First exercise validation error: {e}")
            return False


# 延迟注册，避免在导入时执行
# from .registry import register_validator
# register_validator(1, FirstExerciseValidator())
