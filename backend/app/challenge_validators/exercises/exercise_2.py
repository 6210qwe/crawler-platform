# 第二题验证器：动态字体之变幻
import hashlib
import time
from typing import Any, Dict
from .. import Validator

class Exercise2Validator:
    """第二题验证器：动态字体验证"""
    
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        encoding_key = f"dynamic_{timestamp}"
        
        return {
            "version": "2.1.3",
            "exercise_id": exercise_id,
            "timestamp": timestamp,
            "encodingKey": encoding_key,
            "hint": "字体文件会动态变化，需要实时解析",
            "algorithm": "dynamic_font_encoding"
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
            submitted_encoding_key = payload.get('encodingKey', '')
            
            # 验证时间戳是否在合理范围内（5分钟内）
            current_time = int(time.time())
            if abs(current_time - submitted_timestamp) > 300:  # 5分钟
                return False
            
            # 验证签名
            expected_sign = self._generate_sign(payload)
            if submitted_sign != expected_sign:
                return False
            
            # 验证答案（动态计算：基于时间戳的数字总和）
            answer = getattr(submission, 'answer', 0)
            expected_answer = self._calculate_expected_answer(submitted_timestamp)
            
            return answer == expected_answer
            
        except Exception as e:
            print(f"Exercise 2 validation error: {e}")
            return False
    
    def _generate_sign(self, payload: Dict[str, Any]) -> str:
        """生成签名"""
        # 动态字体签名逻辑
        raw_string = f"{payload.get('answer', 0)}:{payload.get('timeSpent', 0)}:{payload.get('timestamp', 0)}:{payload.get('encodingKey', '')}:dynamic_font"
        return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
    
    def _calculate_expected_answer(self, timestamp: int) -> int:
        """计算期望答案（基于时间戳的动态算法）"""
        # 模拟动态字体数据生成
        total = 0
        for page in range(10):  # 10页
            for pos in range(10):  # 每页10个数字
                # 基于时间戳和位置生成数字
                num = (timestamp + page * 10 + pos) % 100
                total += num
        return total