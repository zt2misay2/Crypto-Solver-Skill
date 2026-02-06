# Crypto-Solver-Skill 集成指南

## 🚀 一分钟快速开始

### 如果你使用 Windows + WSL 环境（推荐）

```bash
# 1. 进入你的 CTF 工作目录
cd /path/to/your/ctf/challenges

# 2. 初始化 Claude Code
npm install -g claude  # 如果未安装

# 3. 安装 Crypto-Solver-Skill
npx skills add <owner>/Crypto-Solver-Skill

# 4. 启动 Claude Code
claude

# 5. 输入你的题目
我有一道 RSA 密码学题目：
[粘贴你的密码题代码]
```

---

## 📋 完整配置步骤

### 步骤 1: 验证环境

**Windows PowerShell** (管理员):

```powershell
# 检查 Python
python3 --version  # 需要 3.8+

# 检查 WSL
wsl --list --verbose

# 验证 WSL 中的 SageMath
wsl sage --version
```

**WSL 中**:

```bash
# 更新包列表
sudo apt update

# 安装 SageMath（第一次可能需要 10+ 分钟）
sudo apt install sagemath

# 安装 Python 依赖
pip3 install gmpy2 sympy pwntools numpy

# 验证
sage -c "print('SageMath OK')"
python3 -c "import gmpy2; print('gmpy2 OK')"
```

### 步骤 2: 设置 Claude Code

```bash
# 全局安装 Claude CLI
npm install -g @anthropic-ai/claude

# 或使用 Codex
npm install -g codex

# 验证安装
claude --version
```

### 步骤 3: 安装 Crypto-Solver-Skill

#### 方式 A: 从 GitHub 仓库

```bash
# 克隆项目
git clone https://github.com/<owner>/Crypto-Solver-Skill.git

# 进入目录
cd Crypto-Solver-Skill

# 为 Claude Code 初始化
npx skills init --ai claude

# 或手动复制到配置目录
mkdir -p ~/.claude/plugins
cp -r . ~/.claude/plugins/crypto-solver
```

#### 方式 B: 通过本地路径

在 Claude Code 配置中添加：

```json
{
  "skills": {
    "crypto-solver": {
      "path": "/path/to/Crypto-Solver-Skill",
      "enabled": true,
      "auto_load": true
    }
  }
}
```

### 步骤 4: 验证安装

```bash
# 启动 Claude Code
claude

# 在 Claude 中运行
/plugin list
# 应该看到 crypto-solver 在列表中

# 或查看配置
/plugin info crypto-solver
```

---

## 💡 使用示例

### 例子 1: RSA 低指数攻击

**输入**:

```
我有一道 RSA 题目，公钥指数 e=3，密文在 output.txt 里。
分析这道题的漏洞并求解。

[题目代码和输出]
```

**AI 工作流**:

```
1️⃣  系统分析
    - 识别 RSA 系统
    - 发现 e=3（低指数）

2️⃣  漏洞识别（暂停等待确认）
    主要漏洞: 低加密指数
    可能的攻击: 直接求立方根

3️⃣  攻击策略（确认后）
    使用 gmpy2.iroot() 求 3 次方根

4️⃣  代码实现
    自动生成 exploit.py

5️⃣  执行结果
    Flag: flag{...}

6️⃣  生成 analyse.md
```

### 例子 2: 椭圆曲线 Pohlig-Hellman 攻击

**输入**:

```
椭圆曲线 ECDLP 题目。曲线参数：
p = ...
a, b = ...
G = (..., ...)
Q = (..., ...)
求离散对数 k，使得 k*G = Q
```

**AI 的分析过程**:

```
✓ 识别为 ECDLP 问题
✓ 分解曲线阶: order = p1^e1 * p2^e2 * ...
✓ 发现小素因子 p1 = 251
✓ 应用 Pohlig-Hellman 攻击
✓ 在子群中求离散对数
✓ 使用 CRT 合并结果
✓ 输出 k 值
```

### 例子 3: 基于 WSL 的 SageMath 计算

**在 Claude Code 中运行**:

```
/skill run-sage

# 以下代码会在 WSL 的 SageMath 中执行
R.<x> = ZZ[]
f = x^3 - 45*x^2 - 117*x + 1215
roots = f.roots()
print(roots)
```

**输出**:

```
[(−9, 1), (5, 1), (49, 1)]
```

---

## 🔧 高级配置

### 自定义超时设置

在 `config.toml` 中修改:

```toml
[timeout]
default = 300      # 通常操作
long_computation = 900  # 格规约等长时间操作
interactive = 20   # 交互式命令
```

### 启用调试模式

在你的项目根目录创建 `.env`:

```bash
CRYPTO_SOLVER_DEBUG=true
CRYPTO_SOLVER_LOG_LEVEL=DEBUG
CRYPTO_SOLVER_TEMP_DIR=/tmp/crypto-solver
```

### 添加自定义攻击模板

1. 在 `templates/attack-templates/` 创建新文件
2. 遵循现有模板格式
3. 在 `prompt.md` 中添加文档

**例**:

```python
# templates/attack-templates/my-attack.py

def my_attack(parameters):
    """我的自定义攻击"""
    pass
```

然后在 prompt.md 中添加：

```markdown
| 我的攻击  | 特定条件 | 相关工具 |
| --------- | -------- | -------- |
| my-attack | 条件描述 | tools    |
```

---

## 🔌 与其他工具集成

### Curve25519（椭圆曲线）

```python
# 使用 pycryptodome 验证
from Cryptodome.PublicKey import ECC

key = ECC.construct(curve="P-256", d=k)
point = key.pointQ
```

### 密钥恢复工具

```python
# 使用 Wiener 攻击库
from owiener import wiener_attack

d = wiener_attack(e, n)
```

### 在线资源

在 Claude Code 中自动调用：

```python
# 自动分解大整数
# API: http://factordb.com/api

import requests
def factor_db(n):
    r = requests.get(f"http://factordb.com/api?n={n}")
    return r.json()
```

---

## 📊 项目集成到现有工作流

### 与 VS Code 的 Debug 功能集成

在 `.vscode/launch.json` 中添加：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Crypto Solver Debug",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/tools/sage-executor.py",
      "console": "integratedTerminal"
    }
  ]
}
```

### 与 Git Workflow 集成

在 `.gitignore` 中添加：

```
.crypto-solver-cache/
*.pth  # pickled sessions
__pycache__/
.pytest_cache/
```

在 `.gitattributes` 中添加：

```
*.sage text eol=lf
*.py text eol=lf
```

---

## 🐛 常见问题

### Q: WSL 中执行 Sage 很慢？

**A**: 这是正常的。优化方法：

- 在 WSL 本地存储 (而不是 /mnt/c)
- 使用 `SAGE_NUM_THREADS=4` 启用并行
- 预加载 SageMath: `sage -n jupyter &`

### Q: "Permission denied" 错误？

**A**: 确保脚本可执行：

```bash
chmod +x tools/sage-executor.py
chmod +x tools/crypto-utils.py
```

### Q: 如何使用代理？

**A**: 在 `config.toml` 中配置：

```toml
[network]
use_proxy = true
proxy_url = "http://proxy.company.com:8080"
```

### Q: 怎样支持中文输出？

**A**: 已默认支持。编码应为 UTF-8：

```python
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

---

## 📞 获取帮助

### 查看日志

```bash
# 查看 Claude Code 日志
cat ~/.claude/logs/debug.log

# 或启用实时调试
claude --debug
```

### 测试 SageMath 集成

```bash
# 创建测试脚本
cat > test_sage.sage << 'EOF'
n = 12345
factors = factor(n)
print(f"Factors: {factors}")
EOF

# 在 WSL 中测试
wsl sage test_sage.sage
```

### 社区支持

- 🐛 报告 Bug: https://github.com/.../issues
- 💬 讨论: https://github.com/.../discussions
- 📧 Email: support@...

---

**需要帮助？**: 查看 [README.md](README.md) 获取完整文档
