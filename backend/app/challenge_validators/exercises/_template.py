# 验证器模板文件
# 复制此文件并重命名为 exercise_X.py，然后修改相应的内容
import hashlib
import time
from typing import Any, Dict
from .. import Validator

class ExerciseTemplateValidator:
    """题目模板验证器"""
    
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        return {
            "version": "1.0.0",
            "exercise_id": exercise_id,
            "timestamp": timestamp,
            "hint": "这是题目模板，请根据实际需求修改",
            # 添加其他公开参数
        }
    
    def validate(self, submission: Any, user: Any, exercise_id: int, public_params: Dict[str, Any]) -> bool:
        """验证提交"""
        try:
            # 获取提交的参数
            payload = getattr(submission, 'payload', {})
            if not payload:
                return False
            
            # 检查必要字段
            if 'timestamp' not in payload or 'sign' not in payload:
                return False
            
            submitted_timestamp = payload['timestamp']
            submitted_sign = payload['sign']
            
            # 验证时间戳是否在合理范围内（5分钟内）
            current_time = int(time.time())
            if abs(current_time - submitted_timestamp) > 300:  # 5分钟
                return False
            
            # 验证签名
            expected_sign = self._generate_sign(payload)
            if submitted_sign != expected_sign:
                return False
            
            # 验证答案
            answer = getattr(submission, 'answer', 0)
            expected_answer = self._calculate_expected_answer()
            
            return answer == expected_answer
            
        except Exception as e:
            print(f"Exercise template validation error: {e}")
            return False
    
    def _generate_sign(self, payload: Dict[str, Any]) -> str:
        """生成签名"""
        # 在这里实现签名逻辑
        raw_string = f"{payload.get('answer', 0)}:{payload.get('timeSpent', 0)}:{payload.get('timestamp', 0)}:template"
        return hashlib.md5(raw_string.encode('utf-8')).hexdigest()
    
    def _calculate_expected_answer(self) -> int:
        """计算期望答案"""
        # 在这里实现答案计算逻辑
        return 0