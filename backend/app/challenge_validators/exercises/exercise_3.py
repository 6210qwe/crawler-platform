# 第三题验证器：字体加密之迷雾
import hashlib
import time
from typing import Any, Dict
from .. import Validator

class Exercise3Validator:
    """第三题验证器：加密字体验证"""
    
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        
        return {
            "version": "3.0.0",
            "exercise_id": exercise_id,
            "timestamp": timestamp,
            "hint": "使用Caesar算法，偏移量为13",
            "algorithm": "Caesar",
            "shift": 13,
            "cipherKey": "ROT13"
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
            expected_sign = self._generate_sign(payload, public_params.get('shift', 13))
            if submitted_sign != expected_sign:
                return False
            
            # 验证答案（加密字体解密后的数字总和）
            answer = getattr(submission, 'answer', 0)
            expected_answer = self._calculate_expected_answer(public_params.get('shift', 13))
            
            return answer == expected_answer
            
        except Exception as e:
            print(f"Exercise 3 validation error: {e}")
            return False
    
    def _generate_sign(self, payload: Dict[str, Any], shift: int) -> str:
        """生成签名"""
        # 加密字体签名逻辑
        raw_string = f"{payload.get('answer', 0)}:{payload.get('timeSpent', 0)}:{payload.get('timestamp', 0)}:{shift}:encrypted_font"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
    
    def _calculate_expected_answer(self, shift: int) -> int:
        """计算期望答案（基于Caesar加密解密）"""
        # 模拟加密数据解密
        encrypted_data = [
            'a1b2c3d4e5',
            'f6g7h8i9j0', 
            'k1l2m3n4o5',
            'p6q7r8s9t0',
            'u1v2w3x4y5'
        ]
        
        total = 0
        for encrypted in encrypted_data:
            # 提取数字部分
            numbers = [int(char) for char in encrypted if char.isdigit()]
            total += sum(numbers)
        
        return total