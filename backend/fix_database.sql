-- 修复数据库表结构
-- 如果exercises表不存在，先创建它
CREATE TABLE IF NOT EXISTS exercises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    challenge_points TEXT NOT NULL,
    tags TEXT,
    points INT NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order INT NOT NULL DEFAULT 0,
    view_count INT NOT NULL DEFAULT 0,
    attempt_count INT NOT NULL DEFAULT 0,
    success_count INT NOT NULL DEFAULT 0,
    avg_time INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_difficulty (difficulty),
    INDEX idx_is_active (is_active)
);

-- 添加缺失的字段（如果不存在）
ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS challenge_points TEXT NOT NULL DEFAULT '';

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS tags TEXT;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS points INT NOT NULL DEFAULT 10;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS sort_order INT NOT NULL DEFAULT 0;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS view_count INT NOT NULL DEFAULT 0;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS attempt_count INT NOT NULL DEFAULT 0;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS success_count INT NOT NULL DEFAULT 0;

ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS avg_time INT;

-- 插入示例数据
INSERT IGNORE INTO exercises (title, description, difficulty, challenge_points, tags, points, sort_order) VALUES
('字体反爬之基础', '识别并绕过基础字体反爬虫技术', '初级', '字体文件分析、字符映射关系、字体替换技术', '["字体反爬", "字体映射", "字符识别"]', 10, 1),
('动态字体之变幻', '处理动态生成的字体文件', '初级', '动态字体分析、字符编码规律、字体缓存机制', '["动态字体", "字体生成", "字符映射"]', 15, 2),
('字体加密之迷雾', '破解加密的字体文件', '中级', '字体加密算法分析、密钥提取、解密实现', '["字体加密", "加密算法", "字体解密"]', 25, 3),
('多字体混淆之复杂', '处理多种字体混合使用的反爬', '中级', '多字体识别、字体切换逻辑、字符对应关系', '["多字体", "字体混淆", "混合字体"]', 30, 4),
('字体变形之扭曲', '识别经过变形的字体字符', '中级', '字体变形算法、字符特征提取、OCR识别优化', '["字体变形", "字符识别", "图像处理"]', 35, 5),
('Cookie基础加密', '识别并破解基础Cookie加密', '初级', 'Cookie结构分析、加密算法识别、解密实现', '["Cookie加密", "基础加密", "Cookie解析"]', 12, 6),
('Cookie时间戳验证', '绕过Cookie时间戳验证', '初级', '时间戳算法、时间同步、Cookie伪造技术', '["时间戳", "时间验证", "Cookie伪造"]', 15, 7),
('AES标准加密', '破解AES标准加密算法', '初级', 'AES算法分析、密钥提取、解密实现', '["AES", "标准加密", "对称加密"]', 15, 8),
('RSA非对称加密', '破解RSA非对称加密', '初级', 'RSA算法分析、密钥分解、私钥提取', '["RSA", "非对称加密", "公钥密码"]', 18, 9),
('Webpack基础分析', '分析Webpack打包的JavaScript代码', '初级', 'Webpack结构分析、模块解析、代码还原', '["Webpack", "模块打包", "代码分析"]', 15, 10);

