#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto-Solver-Skill 初始化脚本
检验环境，配置依赖
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并返回是否成功"""
    try:
        if description:
            print(f"[*] {description}...", end=" ")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            if result.stderr:
                print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ ({str(e)})")
        return False

def check_python():
    """检查 Python 环境"""
    print("\n[*] 检查 Python 环境")
    
    if run_command("python3 --version", "Python 3"):
        version_output = subprocess.run(
            "python3 --version",
            capture_output=True,
            text=True,
            shell=True
        ).stdout
        print(f"    {version_output.strip()}")
    else:
        print("[!] 需要 Python 3.8+")
        return False
    
    return True

def check_sagemath():
    """检查 SageMath"""
    print("\n[*] 检查 SageMath")
    
    # 尝试直接运行 sage
    if run_command("sage --version", "SageMath 直接"):
        return True
    
    # 尝试在 WSL 中运行
    if sys.platform == "win32":
        if run_command("wsl sage --version", "SageMath (WSL)"):
            return True
    
    print("[!] 未找到 SageMath")
    print("    请安装: pip install sagemath")
    print("    或对于 WSL: wsl sudo apt install sagemath")
    return False

def check_python_packages():
    """检查 Python 依赖包"""
    print("\n[*] 检查 Python 包依赖")
    
    packages = {
        "gmpy2": "gmpy2",
        "sympy": "sympy",
        "pwntools": "pwntools",
        "numpy": "numpy"
    }
    
    missing = []
    
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"    ✓ {import_name}")
        except ImportError:
            print(f"    ✗ {import_name} (需要安装)")
            missing.append(package_name)
    
    if missing:
        print(f"\n[*] 安装缺失的包: {', '.join(missing)}")
        cmd = f"pip install {' '.join(missing)}"
        print(f"    运行: {cmd}")
        
        if input("\n继续安装? (y/n): ").lower() == 'y':
            run_command(cmd, "安装依赖包")
        else:
            print("[!] 跳过安装，但某些功能可能不可用")
    
    return len(missing) == 0

def check_directory_structure():
    """检查目录结构"""
    print("\n[*] 检查目录结构")
    
    required_dirs = [
        "tools",
        "templates",
        "templates/attack-templates"
    ]
    
    for dir_name in required_dirs:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"    ✓ {dir_name}/")
        else:
            print(f"    ✗ {dir_name}/ (缺失)")
            return False
    
    return True

def check_skill_files():
    """检查必要的 SKILL 文件"""
    print("\n[*] 检查 SKILL 文件")
    
    required_files = [
        "skill.yaml",
        "prompt.md",
        "README.md",
        "config.toml",
        "tools/sage-executor.py",
        "tools/crypto-utils.py"
    ]
    
    missing = []
    
    for file_name in required_files:
        path = Path(file_name)
        if path.exists():
            print(f"    ✓ {file_name}")
        else:
            print(f"    ✗ {file_name} (缺失)")
            missing.append(file_name)
    
    return len(missing) == 0

def test_sage_execution():
    """测试 SageMath 执行"""
    print("\n[*] 测试 SageMath 执行")
    
    test_code = 'print("SageMath OK")'
    
    try:
        # 创建临时测试文件
        with open("_test_sage.sage", "w") as f:
            f.write(test_code)
        
        cmd = "wsl sage _test_sage.sage" if sys.platform == "win32" else "sage _test_sage.sage"
        
        if run_command(cmd, "执行测试代码"):
            os.remove("_test_sage.sage")
            return True
        else:
            if os.path.exists("_test_sage.sage"):
                os.remove("_test_sage.sage")
            return False
    
    except Exception as e:
        print(f"    ✗ {e}")
        return False

def main():
    """主初始化流程"""
    
    print("=" * 60)
    print("Crypto-Solver-Skill 环境检测")
    print("=" * 60)
    
    results = {
        "Python 环境": check_python(),
        "SageMath": check_sagemath(),
        "Python 包": check_python_packages(),
        "目录结构": check_directory_structure(),
        "SKILL 文件": check_skill_files(),
        "SageMath 执行": test_sage_execution()
    }
    
    # 总结
    print("\n" + "=" * 60)
    print("检测结果总结")
    print("=" * 60)
    
    all_ok = True
    for check, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
        if not result:
            all_ok = False
    
    print("=" * 60)
    
    if all_ok:
        print("\n[✓] 所有检测通过！")
        print("\n你现在可以开始使用 Crypto-Solver-Skill：")
        print("  1. 启动 Claude Code: claude")
        print("  2. 输入你的密码学题目")
        print("  3. AI 会自动选择合适的攻击方法")
        return 0
    else:
        print("\n[!] 某些依赖项未就绪")
        print("\n请修复上述问题后再试。需要帮助？")
        print("  查看 SETUP_GUIDE.md 获取完整安装说明")
        return 1

if __name__ == "__main__":
    sys.exit(main())
