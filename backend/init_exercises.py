#!/usr/bin/env python3
"""
初始化题目数据到数据库
"""
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.exercise import Exercise

# 创建所有表
Base.metadata.create_all(bind=engine)

# 题目数据 - 100道爬虫逆向题目
exercises_data = [
    # 字体反爬 (20道)
    {
        "title": "字体反爬之基础",
        "description": "识别并绕过基础字体反爬虫技术",
        "difficulty": "初级",
        "challenge_points": "字体文件分析、字符映射关系、字体替换技术",
        "tags": ["字体反爬", "字体映射", "字符识别"],
        "points": 10,
        "sort_order": 1
    },
    {
        "title": "动态字体之变幻",
        "description": "处理动态生成的字体文件",
        "difficulty": "初级",
        "challenge_points": "动态字体分析、字符编码规律、字体缓存机制",
        "tags": ["动态字体", "字体生成", "字符映射"],
        "points": 15,
        "sort_order": 2
    },
    {
        "title": "字体加密之迷雾",
        "description": "破解加密的字体文件",
        "difficulty": "中级",
        "challenge_points": "字体加密算法分析、密钥提取、解密实现",
        "tags": ["字体加密", "加密算法", "字体解密"],
        "points": 25,
        "sort_order": 3
    },
    {
        "title": "多字体混淆之复杂",
        "description": "处理多种字体混合使用的反爬",
        "difficulty": "中级",
        "challenge_points": "多字体识别、字体切换逻辑、字符对应关系",
        "tags": ["多字体", "字体混淆", "混合字体"],
        "points": 30,
        "sort_order": 4
    },
    {
        "title": "字体变形之扭曲",
        "description": "识别经过变形的字体字符",
        "difficulty": "中级",
        "challenge_points": "字体变形算法、字符特征提取、OCR识别优化",
        "tags": ["字体变形", "字符识别", "图像处理"],
        "points": 35,
        "sort_order": 5
    },
    {
        "title": "字体随机化之无序",
        "description": "处理随机化字体映射",
        "difficulty": "高级",
        "challenge_points": "随机算法分析、映射规律寻找、动态解析",
        "tags": ["字体随机化", "随机映射", "算法逆向"],
        "points": 45,
        "sort_order": 6
    },
    {
        "title": "字体压缩之精简",
        "description": "处理压缩的字体文件",
        "difficulty": "高级",
        "challenge_points": "压缩算法识别、字体解压、文件结构分析",
        "tags": ["字体压缩", "压缩算法", "文件解析"],
        "points": 50,
        "sort_order": 7
    },
    {
        "title": "字体混淆之复杂",
        "description": "破解高度混淆的字体文件",
        "difficulty": "高级",
        "challenge_points": "混淆算法分析、反混淆技术、字体还原",
        "tags": ["字体混淆", "混淆算法", "反混淆"],
        "points": 55,
        "sort_order": 8
    },
    {
        "title": "字体验证之校验",
        "description": "绕过字体完整性验证",
        "difficulty": "困难",
        "challenge_points": "验证算法分析、校验绕过、字体伪造",
        "tags": ["字体验证", "完整性校验", "绕过技术"],
        "points": 70,
        "sort_order": 9
    },
    {
        "title": "字体动态加载之异步",
        "description": "处理异步动态加载的字体",
        "difficulty": "困难",
        "challenge_points": "异步加载分析、时序控制、字体拦截",
        "tags": ["动态加载", "异步字体", "时序控制"],
        "points": 75,
        "sort_order": 10
    },
    {
        "title": "字体加密之高级",
        "description": "破解高级加密的字体文件",
        "difficulty": "困难",
        "challenge_points": "高级加密算法、密钥破解、解密实现",
        "tags": ["高级加密", "密码学", "字体解密"],
        "points": 80,
        "sort_order": 11
    },
    {
        "title": "字体混淆之终极",
        "description": "破解终极混淆的字体系统",
        "difficulty": "地狱",
        "challenge_points": "复杂混淆算法、系统级逆向、多维度分析",
        "tags": ["终极混淆", "复杂算法", "系统逆向"],
        "points": 120,
        "sort_order": 12
    },
    {
        "title": "字体反调试之保护",
        "description": "绕过字体反调试保护",
        "difficulty": "地狱",
        "challenge_points": "反调试技术、保护机制分析、高级绕过",
        "tags": ["反调试", "保护机制", "绕过技术"],
        "points": 130,
        "sort_order": 13
    },
    {
        "title": "字体多态之变化",
        "description": "处理多态变化的字体",
        "difficulty": "地狱",
        "challenge_points": "多态算法分析、变化模式识别、动态解析",
        "tags": ["多态字体", "动态变化", "模式识别"],
        "points": 140,
        "sort_order": 14
    },
    {
        "title": "字体虚拟机之沙箱",
        "description": "在虚拟机环境中处理字体",
        "difficulty": "地狱",
        "challenge_points": "虚拟机检测、沙箱绕过、环境适配",
        "tags": ["虚拟机", "沙箱环境", "环境检测"],
        "points": 150,
        "sort_order": 15
    },
    {
        "title": "字体云服务之远程",
        "description": "处理云端字体服务",
        "difficulty": "地狱",
        "challenge_points": "云服务分析、网络协议、远程字体处理",
        "tags": ["云服务", "远程字体", "网络分析"],
        "points": 160,
        "sort_order": 16
    },
    {
        "title": "字体AI之智能",
        "description": "处理AI生成的字体",
        "difficulty": "地狱",
        "challenge_points": "AI算法分析、机器学习模型、智能识别技术",
        "tags": ["AI生成", "机器学习", "智能识别"],
        "points": 170,
        "sort_order": 17
    },
    {
        "title": "字体区块链之去中心",
        "description": "处理基于区块链的字体",
        "difficulty": "地狱",
        "challenge_points": "区块链技术、去中心化分析、密码学应用",
        "tags": ["区块链", "去中心化", "密码学"],
        "points": 180,
        "sort_order": 18
    },
    {
        "title": "字体量子之未来",
        "description": "处理量子加密的字体",
        "difficulty": "地狱",
        "challenge_points": "量子加密算法、量子计算原理、未来技术应用",
        "tags": ["量子加密", "量子计算", "未来技术"],
        "points": 200,
        "sort_order": 19
    },
    {
        "title": "字体终极之完美",
        "description": "破解终极完美的字体反爬系统",
        "difficulty": "地狱",
        "challenge_points": "综合技术应用、完美防护分析、终极破解技术",
        "tags": ["终极系统", "完美防护", "综合技术"],
        "points": 250,
        "sort_order": 20
    },

    # Cookie加密 (20道)
    {
        "title": "Cookie基础加密",
        "description": "识别并破解基础Cookie加密",
        "difficulty": "初级",
        "challenge_points": "Cookie结构分析、加密算法识别、解密实现",
        "tags": ["Cookie加密", "基础加密", "Cookie解析"],
        "points": 12,
        "sort_order": 21
    },
    {
        "title": "Cookie时间戳验证",
        "description": "绕过Cookie时间戳验证",
        "difficulty": "初级",
        "challenge_points": "时间戳算法、时间同步、Cookie伪造技术",
        "tags": ["时间戳", "时间验证", "Cookie伪造"],
        "points": 15,
        "sort_order": 22
    },
    {
        "title": "Cookie签名校验",
        "description": "破解Cookie签名校验机制",
        "difficulty": "中级",
        "challenge_points": "签名算法分析、HMAC破解、签名伪造",
        "tags": ["签名校验", "HMAC", "Cookie伪造"],
        "points": 25,
        "sort_order": 23
    },
    {
        "title": "Cookie多重加密",
        "description": "处理多重加密的Cookie",
        "difficulty": "中级",
        "challenge_points": "多重加密分析、解密链构建、嵌套解密",
        "tags": ["多重加密", "嵌套加密", "解密链"],
        "points": 30,
        "sort_order": 24
    },
    {
        "title": "Cookie动态密钥",
        "description": "处理动态密钥的Cookie加密",
        "difficulty": "中级",
        "challenge_points": "密钥生成算法、动态密钥分析、密钥预测",
        "tags": ["动态密钥", "密钥生成", "密钥破解"],
        "points": 35,
        "sort_order": 25
    },
    {
        "title": "Cookie混淆加密",
        "description": "破解混淆的Cookie加密",
        "difficulty": "高级",
        "challenge_points": "混淆算法分析、反混淆技术、加密还原",
        "tags": ["混淆加密", "代码混淆", "反混淆"],
        "points": 45,
        "sort_order": 26
    },
    {
        "title": "Cookie压缩加密",
        "description": "处理压缩加密的Cookie",
        "difficulty": "高级",
        "challenge_points": "压缩算法识别、解压缩技术、加密解密",
        "tags": ["压缩加密", "压缩算法", "解压缩"],
        "points": 50,
        "sort_order": 27
    },
    {
        "title": "Cookie网络传输加密",
        "description": "分析网络传输中的Cookie加密",
        "difficulty": "高级",
        "challenge_points": "网络协议分析、传输加密、协议逆向",
        "tags": ["网络传输", "传输加密", "协议分析"],
        "points": 55,
        "sort_order": 28
    },
    {
        "title": "Cookie反调试保护",
        "description": "绕过Cookie反调试保护",
        "difficulty": "困难",
        "challenge_points": "反调试技术、保护机制分析、高级绕过",
        "tags": ["反调试", "保护机制", "绕过技术"],
        "points": 70,
        "sort_order": 29
    },
    {
        "title": "Cookie虚拟机检测",
        "description": "绕过Cookie虚拟机检测",
        "difficulty": "困难",
        "challenge_points": "虚拟机检测技术、环境伪装、检测绕过",
        "tags": ["虚拟机检测", "环境检测", "绕过技术"],
        "points": 75,
        "sort_order": 30
    },
    {
        "title": "Cookie硬件指纹",
        "description": "处理基于硬件指纹的Cookie",
        "difficulty": "困难",
        "challenge_points": "硬件指纹分析、设备识别算法、指纹伪造技术",
        "tags": ["硬件指纹", "设备识别", "指纹伪造"],
        "points": 80,
        "sort_order": 31
    },
    {
        "title": "Cookie行为分析",
        "description": "绕过Cookie行为分析检测",
        "difficulty": "困难",
        "challenge_points": "行为分析算法、模式识别、行为模拟技术",
        "tags": ["行为分析", "模式识别", "行为模拟"],
        "points": 85,
        "sort_order": 32
    },
    {
        "title": "Cookie机器学习",
        "description": "处理基于机器学习的Cookie",
        "difficulty": "地狱",
        "challenge_points": "机器学习模型分析、AI检测绕过、模型逆向",
        "tags": ["机器学习", "AI检测", "模型分析"],
        "points": 120,
        "sort_order": 33
    },
    {
        "title": "Cookie区块链验证",
        "description": "处理基于区块链的Cookie验证",
        "difficulty": "地狱",
        "challenge_points": "区块链技术、去中心化分析、密码学应用",
        "tags": ["区块链", "去中心化", "密码学"],
        "points": 130,
        "sort_order": 34
    },
    {
        "title": "Cookie量子加密",
        "description": "处理量子加密的Cookie",
        "difficulty": "地狱",
        "challenge_points": "量子加密算法、量子计算原理、量子密码学",
        "tags": ["量子加密", "量子计算", "量子密码"],
        "points": 140,
        "sort_order": 35
    },
    {
        "title": "Cookie生物识别",
        "description": "处理基于生物识别的Cookie",
        "difficulty": "地狱",
        "challenge_points": "生物识别算法、生物特征分析、识别绕过技术",
        "tags": ["生物识别", "生物特征", "识别绕过"],
        "points": 150,
        "sort_order": 36
    },
    {
        "title": "Cookie时空验证",
        "description": "处理时空维度的Cookie验证",
        "difficulty": "地狱",
        "challenge_points": "时空验证算法、多维分析、物理原理应用",
        "tags": ["时空验证", "多维验证", "物理原理"],
        "points": 160,
        "sort_order": 37
    },
    {
        "title": "Cookie意识流检测",
        "description": "处理基于意识流的Cookie检测",
        "difficulty": "地狱",
        "challenge_points": "意识流分析、认知科学原理、意识检测技术",
        "tags": ["意识流", "认知科学", "意识检测"],
        "points": 170,
        "sort_order": 38
    },
    {
        "title": "Cookie平行宇宙",
        "description": "处理平行宇宙中的Cookie",
        "difficulty": "地狱",
        "challenge_points": "平行宇宙理论、多维空间分析、理论物理应用",
        "tags": ["平行宇宙", "多维空间", "理论物理"],
        "points": 180,
        "sort_order": 39
    },
    {
        "title": "Cookie终极完美",
        "description": "破解终极完美的Cookie系统",
        "difficulty": "地狱",
        "challenge_points": "综合技术应用、完美防护分析、终极破解技术",
        "tags": ["终极系统", "完美防护", "综合技术"],
        "points": 200,
        "sort_order": 40
    },

    # 算法加密 (20道)
    {
        "title": "AES标准加密",
        "description": "破解AES标准加密算法",
        "difficulty": "初级",
        "challenge_points": "AES算法分析、密钥提取、解密实现",
        "tags": ["AES", "标准加密", "对称加密"],
        "points": 15,
        "sort_order": 41
    },
    {
        "title": "RSA非对称加密",
        "description": "破解RSA非对称加密",
        "difficulty": "初级",
        "challenge_points": "RSA算法分析、密钥分解、私钥提取",
        "tags": ["RSA", "非对称加密", "公钥密码"],
        "points": 18,
        "sort_order": 42
    },
    {
        "title": "MD5哈希破解",
        "description": "破解MD5哈希算法",
        "difficulty": "初级",
        "challenge_points": "MD5算法分析、哈希碰撞、彩虹表攻击",
        "tags": ["MD5", "哈希算法", "哈希破解"],
        "points": 12,
        "sort_order": 43
    },
    {
        "title": "SHA256哈希分析",
        "description": "分析SHA256哈希算法",
        "difficulty": "中级",
        "challenge_points": "SHA256算法分析、哈希特性、破解技术",
        "tags": ["SHA256", "哈希分析", "密码学"],
        "points": 25,
        "sort_order": 44
    },
    {
        "title": "自研加密算法",
        "description": "逆向分析自研加密算法",
        "difficulty": "中级",
        "challenge_points": "自研算法分析、算法逆向、加密逻辑还原",
        "tags": ["自研算法", "算法逆向", "加密分析"],
        "points": 35,
        "sort_order": 45
    },
    {
        "title": "多重加密嵌套",
        "description": "处理多重嵌套的加密算法",
        "difficulty": "中级",
        "challenge_points": "多重加密分析、嵌套解密、解密链构建",
        "tags": ["多重加密", "嵌套加密", "解密链"],
        "points": 40,
        "sort_order": 46
    },
    {
        "title": "动态加密算法",
        "description": "分析动态变化的加密算法",
        "difficulty": "高级",
        "challenge_points": "动态算法分析、变化规律、动态解密",
        "tags": ["动态加密", "算法变化", "动态分析"],
        "points": 50,
        "sort_order": 47
    },
    {
        "title": "混淆加密算法",
        "description": "破解混淆的加密算法",
        "difficulty": "高级",
        "challenge_points": "混淆算法分析、反混淆技术、加密还原",
        "tags": ["混淆加密", "代码混淆", "反混淆"],
        "points": 55,
        "sort_order": 48
    },
    {
        "title": "硬件加密芯片",
        "description": "分析硬件加密芯片",
        "difficulty": "高级",
        "challenge_points": "硬件加密分析、芯片逆向、硬件破解",
        "tags": ["硬件加密", "芯片分析", "硬件逆向"],
        "points": 60,
        "sort_order": 49
    },
    {
        "title": "量子加密算法",
        "description": "处理量子加密算法",
        "difficulty": "困难",
        "challenge_points": "量子加密算法、量子计算原理、量子密码学",
        "tags": ["量子加密", "量子计算", "量子密码"],
        "points": 80,
        "sort_order": 50
    },
    {
        "title": "生物加密算法",
        "description": "分析生物特征加密算法",
        "difficulty": "困难",
        "challenge_points": "生物加密算法、生物特征分析、生物识别技术",
        "tags": ["生物加密", "生物特征", "生物识别"],
        "points": 85,
        "sort_order": 51
    },
    {
        "title": "混沌加密算法",
        "description": "破解混沌理论加密算法",
        "difficulty": "困难",
        "challenge_points": "混沌理论分析、非线性系统、混沌解密",
        "tags": ["混沌加密", "混沌理论", "非线性系统"],
        "points": 90,
        "sort_order": 52
    },
    {
        "title": "神经网络加密",
        "description": "处理神经网络加密算法",
        "difficulty": "地狱",
        "challenge_points": "神经网络分析、深度学习模型、AI加密破解",
        "tags": ["神经网络", "深度学习", "AI加密"],
        "points": 120,
        "sort_order": 53
    },
    {
        "title": "遗传算法加密",
        "description": "分析遗传算法加密",
        "difficulty": "地狱",
        "challenge_points": "遗传算法分析、进化计算、优化算法逆向",
        "tags": ["遗传算法", "进化计算", "优化算法"],
        "points": 130,
        "sort_order": 54
    },
    {
        "title": "分形加密算法",
        "description": "破解分形几何加密算法",
        "difficulty": "地狱",
        "challenge_points": "分形几何分析、数学算法、分形解密",
        "tags": ["分形加密", "分形几何", "数学算法"],
        "points": 140,
        "sort_order": 55
    },
    {
        "title": "时空加密算法",
        "description": "处理时空维度的加密算法",
        "difficulty": "地狱",
        "challenge_points": "时空加密算法、多维分析、物理原理应用",
        "tags": ["时空加密", "多维加密", "物理原理"],
        "points": 150,
        "sort_order": 56
    },
    {
        "title": "意识流加密",
        "description": "分析基于意识流的加密",
        "difficulty": "地狱",
        "challenge_points": "意识流分析、认知科学原理、意识加密技术",
        "tags": ["意识流", "认知科学", "意识加密"],
        "points": 160,
        "sort_order": 57
    },
    {
        "title": "平行宇宙加密",
        "description": "处理平行宇宙中的加密",
        "difficulty": "地狱",
        "challenge_points": "平行宇宙理论、多维空间分析、理论物理应用",
        "tags": ["平行宇宙", "多维空间", "理论物理"],
        "points": 170,
        "sort_order": 58
    },
    {
        "title": "终极完美加密",
        "description": "破解终极完美的加密系统",
        "difficulty": "地狱",
        "challenge_points": "综合技术应用、完美加密分析、终极破解技术",
        "tags": ["终极系统", "完美加密", "综合技术"],
        "points": 200,
        "sort_order": 59
    },
    {
        "title": "宇宙终极加密",
        "description": "破解宇宙终极加密算法",
        "difficulty": "地狱",
        "challenge_points": "宇宙原理应用、终极算法分析、宇宙级破解技术",
        "tags": ["宇宙加密", "终极算法", "宇宙原理"],
        "points": 250,
        "sort_order": 60
    },

    # Webpack (20道)
    {
        "title": "Webpack基础分析",
        "description": "分析Webpack打包的JavaScript代码",
        "difficulty": "初级",
        "challenge_points": "Webpack结构分析、模块解析、代码还原",
        "tags": ["Webpack", "模块打包", "代码分析"],
        "points": 15,
        "sort_order": 61
    },
    {
        "title": "Webpack模块映射",
        "description": "解析Webpack模块映射关系",
        "difficulty": "初级",
        "challenge_points": "模块映射分析、依赖关系、模块还原",
        "tags": ["模块映射", "依赖分析", "模块解析"],
        "points": 18,
        "sort_order": 62
    },
    {
        "title": "Webpack代码分割",
        "description": "处理Webpack代码分割",
        "difficulty": "中级",
        "challenge_points": "代码分割分析、懒加载机制、动态导入处理",
        "tags": ["代码分割", "懒加载", "动态导入"],
        "points": 25,
        "sort_order": 63
    },
    {
        "title": "Webpack Tree Shaking",
        "description": "分析Webpack Tree Shaking",
        "difficulty": "中级",
        "challenge_points": "Tree Shaking分析、死代码识别、优化还原",
        "tags": ["Tree Shaking", "死代码消除", "优化分析"],
        "points": 28,
        "sort_order": 64
    },
    {
        "title": "Webpack插件系统",
        "description": "分析Webpack插件系统",
        "difficulty": "中级",
        "challenge_points": "插件系统分析、钩子函数、插件逆向",
        "tags": ["插件系统", "插件分析", "钩子函数"],
        "points": 32,
        "sort_order": 65
    },
    {
        "title": "Webpack混淆代码",
        "description": "处理Webpack混淆的代码",
        "difficulty": "高级",
        "challenge_points": "混淆算法分析、反混淆技术、代码还原",
        "tags": ["代码混淆", "混淆分析", "反混淆"],
        "points": 45,
        "sort_order": 66
    },
    {
        "title": "Webpack压缩优化",
        "description": "分析Webpack压缩优化",
        "difficulty": "高级",
        "challenge_points": "压缩算法分析、优化还原、代码美化",
        "tags": ["代码压缩", "优化分析", "压缩还原"],
        "points": 48,
        "sort_order": 67
    },
    {
        "title": "Webpack动态加载",
        "description": "处理Webpack动态加载",
        "difficulty": "高级",
        "challenge_points": "动态加载分析、异步模块处理、加载机制",
        "tags": ["动态加载", "异步模块", "加载分析"],
        "points": 52,
        "sort_order": 68
    },
    {
        "title": "Webpack热更新",
        "description": "分析Webpack热更新机制",
        "difficulty": "困难",
        "challenge_points": "热更新机制、HMR分析、实时更新处理",
        "tags": ["热更新", "HMR", "实时更新"],
        "points": 70,
        "sort_order": 69
    },
    {
        "title": "Webpack多入口",
        "description": "处理Webpack多入口配置",
        "difficulty": "困难",
        "challenge_points": "多入口分析、配置解析、入口处理",
        "tags": ["多入口", "入口分析", "配置解析"],
        "points": 75,
        "sort_order": 70
    },
    {
        "title": "Webpack环境变量",
        "description": "分析Webpack环境变量",
        "difficulty": "困难",
        "challenge_points": "环境变量分析、配置解析、变量处理",
        "tags": ["环境变量", "配置分析", "变量解析"],
        "points": 80,
        "sort_order": 71
    },
    {
        "title": "Webpack自定义Loader",
        "description": "分析Webpack自定义Loader",
        "difficulty": "困难",
        "challenge_points": "自定义Loader分析、转换器逆向、Loader处理",
        "tags": ["自定义Loader", "Loader分析", "转换器"],
        "points": 85,
        "sort_order": 72
    },
    {
        "title": "Webpack微前端",
        "description": "处理Webpack微前端架构",
        "difficulty": "地狱",
        "challenge_points": "微前端架构分析、模块联邦、架构逆向",
        "tags": ["微前端", "架构分析", "模块联邦"],
        "points": 120,
        "sort_order": 73
    },
    {
        "title": "Webpack SSR",
        "description": "分析Webpack服务端渲染",
        "difficulty": "地狱",
        "challenge_points": "SSR分析、服务端渲染、同构应用处理",
        "tags": ["SSR", "服务端渲染", "同构应用"],
        "points": 130,
        "sort_order": 74
    },
    {
        "title": "Webpack PWA",
        "description": "处理Webpack PWA应用",
        "difficulty": "地狱",
        "challenge_points": "PWA分析、渐进式应用、离线缓存处理",
        "tags": ["PWA", "渐进式应用", "离线缓存"],
        "points": 140,
        "sort_order": 75
    },
    {
        "title": "Webpack WebAssembly",
        "description": "分析Webpack WebAssembly集成",
        "difficulty": "地狱",
        "challenge_points": "WebAssembly分析、WASM处理、二进制模块",
        "tags": ["WebAssembly", "WASM", "二进制模块"],
        "points": 150,
        "sort_order": 76
    },
    {
        "title": "Webpack量子计算",
        "description": "处理Webpack量子计算集成",
        "difficulty": "地狱",
        "challenge_points": "量子计算分析、量子算法、量子模块处理",
        "tags": ["量子计算", "量子算法", "量子模块"],
        "points": 160,
        "sort_order": 77
    },
    {
        "title": "Webpack时空模块",
        "description": "分析Webpack时空维度模块",
        "difficulty": "地狱",
        "challenge_points": "时空模块分析、多维处理、物理原理应用",
        "tags": ["时空模块", "多维模块", "物理原理"],
        "points": 170,
        "sort_order": 78
    },
    {
        "title": "Webpack意识流模块",
        "description": "处理Webpack意识流模块",
        "difficulty": "地狱",
        "challenge_points": "意识流分析、认知模块、意识处理技术",
        "tags": ["意识流", "认知模块", "意识处理"],
        "points": 180,
        "sort_order": 79
    },
    {
        "title": "Webpack终极完美",
        "description": "破解Webpack终极完美系统",
        "difficulty": "地狱",
        "challenge_points": "综合技术应用、完美架构分析、终极破解技术",
        "tags": ["终极系统", "完美架构", "综合技术"],
        "points": 200,
        "sort_order": 80
    },

    # 代码混淆 (20道)
    {
        "title": "标准Obfuscator混淆",
        "description": "破解标准Obfuscator混淆",
        "difficulty": "初级",
        "challenge_points": "Obfuscator分析、标准混淆、反混淆技术",
        "tags": ["Obfuscator", "标准混淆", "反混淆"],
        "points": 20,
        "sort_order": 81
    },
    {
        "title": "魔改Obfuscator混淆",
        "description": "破解魔改版Obfuscator混淆",
        "difficulty": "中级",
        "challenge_points": "魔改混淆分析、定制算法、混淆变异处理",
        "tags": ["魔改混淆", "定制混淆", "混淆变异"],
        "points": 35,
        "sort_order": 82
    },
    {
        "title": "自研混淆算法",
        "description": "逆向分析自研混淆算法",
        "difficulty": "高级",
        "challenge_points": "自研算法分析、混淆逆向、算法还原",
        "tags": ["自研混淆", "算法逆向", "混淆分析"],
        "points": 50,
        "sort_order": 83
    },
    {
        "title": "JSVMP虚拟机混淆",
        "description": "破解JSVMP虚拟机混淆",
        "difficulty": "高级",
        "challenge_points": "JSVMP分析、虚拟机逆向、字节码处理",
        "tags": ["JSVMP", "虚拟机混淆", "字节码"],
        "points": 60,
        "sort_order": 84
    },
    {
        "title": "多重混淆嵌套",
        "description": "处理多重嵌套的混淆",
        "difficulty": "困难",
        "challenge_points": "多重混淆分析、嵌套处理、混淆链破解",
        "tags": ["多重混淆", "嵌套混淆", "混淆链"],
        "points": 80,
        "sort_order": 85
    },
    {
        "title": "动态混淆算法",
        "description": "分析动态变化的混淆",
        "difficulty": "困难",
        "challenge_points": "动态混淆分析、变化规律、动态破解",
        "tags": ["动态混淆", "混淆变化", "动态分析"],
        "points": 85,
        "sort_order": 86
    },
    {
        "title": "硬件混淆保护",
        "description": "绕过硬件混淆保护",
        "difficulty": "困难",
        "challenge_points": "硬件混淆分析、硬件保护、绕过技术",
        "tags": ["硬件混淆", "硬件保护", "绕过技术"],
        "points": 90,
        "sort_order": 87
    },
    {
        "title": "量子混淆算法",
        "description": "处理量子混淆算法",
        "difficulty": "地狱",
        "challenge_points": "量子混淆分析、量子计算、量子算法处理",
        "tags": ["量子混淆", "量子计算", "量子算法"],
        "points": 120,
        "sort_order": 88
    },
    {
        "title": "生物混淆算法",
        "description": "分析生物特征混淆",
        "difficulty": "地狱",
        "challenge_points": "生物混淆分析、生物特征、生物算法处理",
        "tags": ["生物混淆", "生物特征", "生物算法"],
        "points": 130,
        "sort_order": 89
    },
    {
        "title": "混沌混淆系统",
        "description": "破解混沌理论混淆",
        "difficulty": "地狱",
        "challenge_points": "混沌理论分析、非线性系统、混沌破解",
        "tags": ["混沌混淆", "混沌理论", "非线性系统"],
        "points": 140,
        "sort_order": 90
    },
    {
        "title": "神经网络混淆",
        "description": "处理神经网络混淆",
        "difficulty": "地狱",
        "challenge_points": "神经网络分析、深度学习、AI混淆处理",
        "tags": ["神经网络", "深度学习", "AI混淆"],
        "points": 150,
        "sort_order": 91
    },
    {
        "title": "遗传算法混淆",
        "description": "分析遗传算法混淆",
        "difficulty": "地狱",
        "challenge_points": "遗传算法分析、进化计算、优化混淆处理",
        "tags": ["遗传算法", "进化计算", "优化混淆"],
        "points": 160,
        "sort_order": 92
    },
    {
        "title": "分形混淆几何",
        "description": "破解分形几何混淆",
        "difficulty": "地狱",
        "challenge_points": "分形几何分析、数学混淆、分形破解",
        "tags": ["分形混淆", "分形几何", "数学混淆"],
        "points": 170,
        "sort_order": 93
    },
    {
        "title": "时空混淆维度",
        "description": "处理时空维度混淆",
        "difficulty": "地狱",
        "challenge_points": "时空混淆分析、多维处理、物理混淆技术",
        "tags": ["时空混淆", "多维混淆", "物理混淆"],
        "points": 180,
        "sort_order": 94
    },
    {
        "title": "意识流混淆",
        "description": "分析意识流混淆",
        "difficulty": "地狱",
        "challenge_points": "意识流分析、认知混淆、意识处理技术",
        "tags": ["意识流", "认知混淆", "意识处理"],
        "points": 190,
        "sort_order": 95
    },
    {
        "title": "平行宇宙混淆",
        "description": "处理平行宇宙混淆",
        "difficulty": "地狱",
        "challenge_points": "平行宇宙分析、多维混淆、理论混淆技术",
        "tags": ["平行宇宙", "多维混淆", "理论混淆"],
        "points": 200,
        "sort_order": 96
    },
    {
        "title": "终极完美混淆",
        "description": "破解终极完美混淆",
        "difficulty": "地狱",
        "challenge_points": "综合混淆技术、完美混淆分析、终极破解",
        "tags": ["终极混淆", "完美混淆", "综合混淆"],
        "points": 220,
        "sort_order": 97
    },
    {
        "title": "宇宙终极混淆",
        "description": "破解宇宙终极混淆",
        "difficulty": "地狱",
        "challenge_points": "宇宙原理应用、终极混淆分析、宇宙级破解",
        "tags": ["宇宙混淆", "终极混淆", "宇宙原理"],
        "points": 250,
        "sort_order": 98
    },
    {
        "title": "无限递归混淆",
        "description": "处理无限递归混淆",
        "difficulty": "地狱",
        "challenge_points": "递归混淆分析、无限循环处理、递归破解技术",
        "tags": ["递归混淆", "无限循环", "递归破解"],
        "points": 300,
        "sort_order": 99
    },
    {
        "title": "完美终极混淆",
        "description": "破解完美终极混淆系统",
        "difficulty": "地狱",
        "challenge_points": "完美系统分析、终极混淆技术、完美破解方法",
        "tags": ["完美系统", "终极混淆", "完美破解"],
        "points": 500,
        "sort_order": 100
    }
]

def init_exercises():
    """初始化题目数据"""
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(Exercise).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 道题目，跳过初始化")
            return
        
        # 插入题目数据
        for exercise_data in exercises_data:
            exercise = Exercise(
                title=exercise_data["title"],
                description=exercise_data["description"],
                difficulty=exercise_data["difficulty"],
                challenge_points=exercise_data["challenge_points"],
                tags=json.dumps(exercise_data["tags"], ensure_ascii=False),
                points=exercise_data["points"],
                sort_order=exercise_data["sort_order"],
                is_active=True
            )
            db.add(exercise)
        
        db.commit()
        print(f"成功初始化 {len(exercises_data)} 道题目")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_exercises()
