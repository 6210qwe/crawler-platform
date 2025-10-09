# 题目模块系统使用说明

## 🎯 系统概述

这是一个模块化的题目系统，每个题目都有独立的逻辑文件，便于后期维护和扩展。

## 📁 文件结构

```
exercise-mods/
├── types.ts              # 类型定义
├── _template/            # 模板目录
│   └── mod.ts           # 题目模板
├── 1/                   # 第一题：字体反爬之基础
│   └── mod.ts
├── 2/                   # 第二题：动态字体之变幻
│   └── mod.ts
├── 3/                   # 第三题：字体加密之迷雾
│   └── mod.ts
└── README.md            # 使用说明
```

## 🔧 如何添加新题目

### 1. 创建前端题目模块

1. 复制 `_template/mod.ts` 到新目录 `{题目ID}/mod.ts`
2. 修改题目信息：

```typescript
const mod: ExerciseMod = {
  version: '1.0.0',
  
  async prepare(ctx: PrepareContext) {
    // 返回题目特定的公开参数
    return {
      timestamp: Math.floor(Date.now() / 1000),
      hint: '你的题目提示'
    }
  },
  
  async signRequest(input: SignInput): Promise<SignResult> {
    // 实现签名逻辑
    const timestamp = Math.floor(Date.now() / 1000)
    const rawString = `${input.answer}:${input.timeSpent}:${timestamp}:your_secret`
    const sign = CryptoJS.MD5(rawString).toString()
    
    return {
      version: '1.0.0',
      payload: { answer: input.answer, timeSpent: input.timeSpent, timestamp },
      sign,
      timestamp
    }
  },
  
  renderHints() {
    // 返回题目提示UI
    return React.createElement('div', { className: 'your-hint-styles' }, [
      // 你的提示内容
    ])
  }
}
```

### 2. 创建后端验证器

1. 复制 `backend/app/challenge_validators/exercises/_template.py` 到 `exercise_X.py`
2. 修改验证器类：

```python
class ExerciseXValidator:
    def get_public_params(self, user: Any, exercise_id: int) -> Dict[str, Any]:
        """返回公开参数"""
        timestamp = int(time.time())
        return {
            "version": "1.0.0",
            "exercise_id": exercise_id,
            "timestamp": timestamp,
            "hint": "你的题目提示"
        }
    
    def validate(self, submission: Any, user: Any, exercise_id: int, public_params: Dict[str, Any]) -> bool:
        """验证提交"""
        try:
            payload = getattr(submission, 'payload', {})
            if not payload:
                return False
            
            # 验证时间戳
            current_time = int(time.time())
            if abs(current_time - payload.get('timestamp', 0)) > 300:
                return False
            
            # 验证签名
            expected_sign = self._generate_sign(payload)
            if payload.get('sign') != expected_sign:
                return False
            
            # 验证答案
            answer = getattr(submission, 'answer', 0)
            expected_answer = self._calculate_expected_answer()
            
            return answer == expected_answer
            
        except Exception as e:
            print(f"Exercise X validation error: {e}")
            return False
    
    def _generate_sign(self, payload: Dict[str, Any]) -> str:
        """生成签名"""
        raw_string = f"{payload.get('answer', 0)}:{payload.get('timeSpent', 0)}:{payload.get('timestamp', 0)}:your_secret"
        return hashlib.md5(raw_string.encode('utf-8')).hexdigest()
    
    def _calculate_expected_answer(self) -> int:
        """计算期望答案"""
        # 实现你的答案计算逻辑
        return 0
```

3. 在 `registry.py` 中注册验证器：

```python
from .exercises.exercise_X import ExerciseXValidator

def auto_register_validators():
    register_validator(X, ExerciseXValidator())
```

## 🎨 题目示例

### 第一题：字体反爬之基础
- **功能**：MD5参数验证
- **特点**：翻页时需要携带 `MD5(timestamp + "spider")` 参数
- **验证**：时间戳验证 + MD5签名验证 + 答案验证

### 第二题：动态字体之变幻
- **功能**：动态字体验证
- **特点**：字体文件会随时间变化，需要实时解析
- **验证**：动态编码密钥 + SHA256签名 + 基于时间戳的答案计算

### 第三题：字体加密之迷雾
- **功能**：加密字体验证
- **特点**：使用Caesar算法，偏移量为13
- **验证**：加密算法验证 + 解密逻辑 + 答案验证

## 🔍 调试技巧

1. **前端调试**：
   - 使用浏览器开发者工具查看网络请求
   - 在题目模块中添加 `console.log` 输出调试信息
   - 检查签名生成是否正确

2. **后端调试**：
   - 在后端日志中查看验证器执行情况
   - 使用 `print` 语句输出调试信息
   - 检查签名验证逻辑

3. **常见问题**：
   - 时间戳超时：检查时间同步
   - 签名验证失败：检查签名算法是否一致
   - 答案错误：检查答案计算逻辑

## 📝 最佳实践

1. **安全性**：
   - 使用强签名算法（MD5、SHA256等）
   - 设置合理的时间戳超时时间
   - 避免在客户端暴露敏感信息

2. **性能**：
   - 避免在题目模块中执行重操作
   - 合理使用缓存机制
   - 优化签名计算

3. **维护性**：
   - 为每个题目添加清晰的注释
   - 使用有意义的变量名
   - 保持代码结构清晰

## 🚀 扩展功能

系统支持以下扩展功能：

- **自定义UI渲染**：可以完全自定义题目的显示界面
- **复杂验证逻辑**：支持多种加密算法和验证方式
- **动态参数**：支持基于时间、用户等动态参数
- **提示系统**：可以为用户提供题目相关的提示信息

## 📞 技术支持

如果在使用过程中遇到问题，请：

1. 检查控制台错误信息
2. 查看后端日志
3. 参考示例题目的实现
4. 检查类型定义是否正确