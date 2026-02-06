# Crypto-Solver-Skill: CTF 密码学自动求解 SKILL

> 为 Claude Code、Codex、Cursor 等 AI IDE 专设的密码学 CTF 题目快速求解工具

## 📋 特性

✅ **完整的密码学知识库**

- RSA 攻击决策表（10+ 种攻击方法）
- 椭圆曲线 (ECC) 漏洞识别
- 格密码 (Lattice) 攻击
- 对称加密模式破解

✅ **自动化工作流**

1. 系统分析 → 漏洞识别 → 攻击策略 → 代码实现 → 文档生成
2. 内置暂停点，等待用户确认关键决策

✅ **SageMath 集成**

- WSL 中直接执行 SageMath 代码
- Python 和 SageMath 无缝协作
- 自动处理超时和错误

✅ **即插即用**

- 一行命令安装
- 与 Claude Code、Cursor 等无缝集成
- 无需额外配置

---

## Codex (专用)

这个仓库已包含 **Codex 可识别的 `SKILL.md`**（与本仓库里的 `skill.yaml`/`prompt.md` 等并存，不影响其它平台）。

### 安装

Codex 会从 `$CODEX_HOME/skills`（默认 `~/.codex/skills`）加载 skills。把本仓库放到该目录即可：

```bash
# 默认 CODEX_HOME=~/.codex
mkdir -p ~/.codex/skills/crypto-solver-skill
git clone https://github.com/zt2misay2/Crypto-Solver-Skill.git ~/.codex/skills/crypto-solver-skill
# 或者如果已 clone：更新
cd ~/.codex/skills/crypto-solver-skill && git pull
```

然后重启 Codex。

### 使用

在 Codex 对话里直接提：`使用 crypto-solver-skill` 或描述你的密码学题目并贴出源码/输出，按 `SKILL.md` 的 Phase 流程推进。

## 🚀 安装

### 方式 1: 通过 npm Skills（推荐）

```bash
# 进入你的项目目录
cd /path/to/your/project

# 安装 Crypto-Solver-Skill
npx skills add <owner>/Crypto-Solver-Skill

# 或在 Claude Code 中执行
/plugin install crypto-solver
```

### 方式 2: 本地安装

```bash
# 克隆仓库到本地
git clone https://github.com/<owner>/Crypto-Solver-Skill.git

# 进入项目
cd Crypto-Solver-Skill

# 为 Claude Code 配置
uipro init --ai claude

# 为 Cursor 配置
uipro init --ai cursor

# 为所有 AI 助手配置
uipro init --ai all
```

### 方式 3: 手动集成到现有项目

```bash
# 复制 SKILL 文件到项目中
mkdir -p .claude/skills
cp -r Crypto-Solver-Skill/* .claude/skills/crypto-solver/

# 或作为子模块
git submodule add https://github.com/<owner>/Crypto-Solver-Skill.git .claude/skills/crypto-solver
```

---

## 🎯 快速开始

### 1. 在 Claude Code 中激活

打开你的 CTF 题目，输入：

```
我需要解决密码学赛题。这是密码系统的源代码：

[粘贴密码学源代码]

请帮我分析漏洞并获取 Flag。
```

AI 会自动进入 **Crypto 工作流模式**，按照以下步骤：

### 2. Phase 1: 系统分析

AI 会：

- 📖 读取所有源代码
- 🔍 识别加密算法和参数
- 📊 绘制加密流程图
- 📝 输出系统分析报告

**示例输出**:

```
## 密码学系统分析

**加密算法**: RSA (n=2048bit, e=3)
**密钥生成**: 标准 RSA 密钥生成
**加密流程**: flag → RSA 加密 → 密文
**特殊修改**: e=3（很小）可能存在低指数攻击
```

### 3. Phase 2: 漏洞识别

AI 会分析并提出：

```
## 漏洞分析

**主要弱点**: 公钥指数 e=3，满足低加密指数条件

**可利用点**:
- e=3 很小
- 只进行单次加密
- flag 可能满足 flag^3 < n

**初步思路**: 直接求 3 次立方根可获取明文
```

**⚠️ 此时会暂停，等待你的确认或补充信息**

### 4. Phase 3: 攻击策略

确认后，AI 生成详细攻击计划：

```
## 攻击方案

**核心思路**: 低加密指数攻击 - 直接求立方根

**实施步骤**:
1. 从输出中提取密文 c
2. 计算 m = cbrt(c)  （c 的立方根）
3. 将 m 转换为字符串获取 Flag

**所需工具**: gmpy2 库用于高精度计算
```

### 5. Phase 4: 代码实现

AI 自动生成可执行代码：

```python
# exploit.py - 一行命令执行
from gmpy2 import iroot

n = 0x...
e = 3
c = 0x...

m = int(iroot(c, e)[0])
flag = bytes.fromhex(hex(m)[2:])
print(f"Flag: {flag.decode()}")
```

**执行**:

```bash
python exploit.py
```

### 6. Phase 5: 文档生成

生成完整 `analyse.md`：

```markdown
# RSA 低加密指数攻击 题解

## A. 问题结构

...

## B. 求解思路

数学推导和公式说明

## C. 解题代码

完整的 Python 代码和运行结果

## D. 总结反思

...
```

---

## 📚 支持的攻击类型

### RSA 系列

| 攻击        | 条件                  | 复杂度    | 代码位置                   |
| ----------- | --------------------- | --------- | -------------------------- |
| 低加密指数  | e=3, m^e<n            | O(1)      | `low-exponent-attack.py`   |
| Håstad 广播 | 同消息 k 次加密 (k=e) | O(log²n)  | `low-exponent-attack.py`   |
| 公共模数    | gcd(e1,e2)=1          | O(log n)  | `common-modulus-attack.py` |
| Fermat 分解 | $\|p-q\|$ 小          | O(√(q-p)) | `fermat-factorization.py`  |
| Wiener 攻击 | d < n^0.25            | O(log³n)  | -                          |

### 椭圆曲线 (ECC) 系列

| 攻击           | 条件             | 方法           |
| -------------- | ---------------- | -------------- |
| Pohlig-Hellman | 曲线阶有小因子   | 分步求离散对数 |
| Smart 攻击     | j-invariant 特殊 | p-adic lifting |
| Invalid Curve  | 点不在曲线上     | 利用计算差异   |

### 对称加密系列

| 模式 | 漏洞           | 攻击方法     |
| ---- | -------------- | ------------ |
| ECB  | 模式重复       | 频率分析     |
| CBC  | Padding Oracle | 字节翻转恢复 |
| CTR  | Nonce 重用     | 密钥流恢复   |

---

## 🛠 命令参考

### 在 Claude Code 中使用

**分析密码系统**:

```
/skill analyze-crypto secret.py
```

**自动生成攻击代码**:

```
/skill generate-attack low-exponent
/skill generate-attack common-modulus
/skill generate-attack fermat-factorization
```

**执行 SageMath 代码**:

```
/skill run-sage

# 输入或粘贴代码
def factor_using_sage(n):
    return factor(n)

# Ctrl+D 执行
```

**一键求解**:

```
/skill solve-challenge challenge.tar.gz
```

---

## 📦 项目文件结构

```
Crypto-Solver-Skill/
├── skill.yaml                          # 核心配置
├── prompt.md                           # 知识库和工作流
├── README.md                           # 本文件
├── tools/
│   ├── sage-executor.py               # SageMath 执行工具
│   └── crypto-utils.py                # 通用密码学工具
└── templates/
    └── attack-templates/
        ├── low-exponent-attack.py     # 低指数攻击
        ├── common-modulus-attack.py   # 公共模数攻击
        └── fermat-factorization.py    # Fermat 分解
```

---

## 🔧 依赖项

### 必需

- Python 3.8+
- SageMath 9.0+

### 推荐

```bash
# Python 包
pip install gmpy2 sympy pwntools numpy

# WSL 中 SageMath
wsl sudo apt install sagemath
```

### 验证安装

```bash
# 验证 Python
python3 --version

# 验证 Sage
wsl sage --version

# 验证依赖
python3 -c "import gmpy2, sympy; print('OK')"
```

---

## ⚡ 高级用法

### 自定义攻击模板

在 `templates/attack-templates/` 中添加新文件：

```python
# my-custom-attack.py
def my_attack(parameters):
    """你的自定义攻击实现"""
    pass
```

AI 会自动发现并在合适时推荐。

### 集成 SageMath 高级功能

```python
# 直接在 Claude Code 中调用
/skill run-sage

# 使用您的自定义 SageMath 脚本
from sage.all import *

# 格规约
M = Matrix([[1,0,1039],[0,1,3]])
M_reduced = M.LLL()
print(M_reduced)
```

### 与其他密码工具集成

```python
# 可集成的工具
- FactorDB API (在线因子分解)
- Wolfram Alpha (高级计算)
- 自定义 Oracle 接口 (动态题目)
```

---

## 🐛 故障排除

### 问题：模块导入错误

**错误**:

```
ModuleNotFoundError: No module named 'gmpy2'
```

**解决**:

```bash
pip install gmpy2 -U
# 或从源编译
pip install gmpy2 --no-binary gmpy2
```

### 问题：Sage 命令未找到

**错误**:

```
sage: command not found
```

**解决**:

```bash
# 在 WSL 中验证
wsl which sage

# 或指定完整路径
~/.local/bin/sage  # Conda 安装
# /opt/sagemath/bin/sage  # 其他安装方式
```

### 问题：超时错误

**症状**: 计算超过 5 分钟

**解决**:

1. 减少迭代次数
2. 使用更快的算法
3. 手动增加超时设施：
   ```yaml
   timeout: 600 # 10 分钟
   ```

---

## 📖 学习资源

### 推荐资料

- Cryptohack: https://cryptohack.org/
- CTF Time: https://ctftime.org/
- FactorDB: http://factordb.com/

### 学术参考

- Handbook of Elliptic and Hyperelliptic Curve Cryptography
- A Course in Number Theory and Cryptography (Koblitz)
- Handbook of Finite Fields and Applications

---

## 🤝 贡献

欢迎贡献新的攻击模板！

1. Fork 项目
2. 在 `templates/attack-templates/` 中添加新文件
3. 更新 `prompt.md` 的攻击表
4. 提交 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 💬 反馈和支持

有问题或建议？

- 📧 Email: support@example.com
- 🐛 Issue: https://github.com/example/issues
- 💬 Discussions: https://github.com/example/discussions

---

## 🎓 引用

如果你在学术工作中使用此工具，请引用：

```bibtex
@software{crypto_solver_skill_2026,
  title={Crypto-Solver-Skill: CTF Cryptography Solver for AI IDEs},
  author={Your Name},
  year={2026},
  url={https://github.com/example/Crypto-Solver-Skill}
}
```

---

**版本**: 1.0.0  
**最后更新**: 2026-02-06  
**状态**: 🟢 维护中
