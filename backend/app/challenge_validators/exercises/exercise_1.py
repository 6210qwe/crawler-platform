# 第一题验证器：字体反爬之基础
import hashlib
import time
from typing import Any, Dict
from .. import Validator

class Exercise1Validator:
    """第一题验证器：MD5参数验证"""
    
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        return {
            "version": "1.0.0",
            "exercise_id": exercise_id,
            "timestamp": timestamp,
            "hint": "翻页时需要携带 MD5(timestamp + 'spider') 参数"
        }
    
    def validate(self, submission: Any, user: Any, exercise_id: int, public_params: Dict[str, Any]) -> bool:
        """验证提交"""
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
            
            # 验证答案是否正确（这里只验证MD5参数，不验证具体答案）
            # 具体答案验证由后端主逻辑处理
            return True
            
        except Exception as e:
            print(f"Exercise 1 validation error: {e}")
            return False