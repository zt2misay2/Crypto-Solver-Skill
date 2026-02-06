#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SageMath 代码执行工具
支持在 WSL 中执行 SageMath 代码并返回结果
"""

import subprocess
import sys
import json
import tempfile
import os
import platform
from pathlib import Path
from typing import Dict, Any

class SageExecutor:
    """SageMath 代码执行器"""
    
    def __init__(self, use_wsl: bool = True):
        self.use_wsl = use_wsl and platform.system() == "Windows"
        self.sage_command = self._get_sage_command()
    
    def _get_sage_command(self) -> list:
        """获取 SageMath 执行命令"""
        if self.use_wsl:
            return ['wsl', 'sage']
        else:
            return ['sage']
    
    def execute(self, code: str, timeout: int = 300) -> Dict[str, Any]:
        """
        执行 SageMath 代码
        
        Args:
            code: SageMath 代码字符串
            timeout: 超时时间（秒）
        
        Returns:
            {
                "success": bool,
                "output": str,
                "error": str,
                "code": int
            }
        """
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.sage', 
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            cmd = self.sage_command + [temp_file]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout,
                text=True,
                encoding='utf-8'
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "code": result.returncode,
                "status": "completed" if result.returncode == 0 else "error"
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"执行超时 ({timeout} 秒)",
                "code": -1,
                "status": "timeout"
            }
        
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "code": -2,
                "status": "error"
            }
        
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def execute_file(self, file_path: str, timeout: int = 300) -> Dict[str, Any]:
        """
        执行 SageMath 文件
        
        Args:
            file_path: .sage 文件路径
            timeout: 超时时间（秒）
        
        Returns:
            执行结果字典
        """
        
        if not os.path.exists(file_path):
            return {
                "success": False,
                "output": "",
                "error": f"文件不存在: {file_path}",
                "code": -1,
                "status": "error"
            }
        
        try:
            cmd = self.sage_command + [file_path]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout,
                text=True,
                encoding='utf-8'
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "code": result.returncode,
                "file": file_path,
                "status": "completed" if result.returncode == 0 else "error"
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"执行超时 ({timeout} 秒)",
                "code": -1,
                "file": file_path,
                "status": "timeout"
            }
        
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "code": -2,
                "file": file_path,
                "status": "error"
            }


def main():
    """命令行入口"""
    
    executor = SageExecutor(use_wsl=True)
    
    # 从标准输入读取代码
    code = sys.stdin.read()
    
    if not code.strip():
        print(json.dumps({
            "success": False,
            "error": "未提供代码",
            "code": -1
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    result = executor.execute(code)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
