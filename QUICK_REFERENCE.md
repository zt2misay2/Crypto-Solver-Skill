# Crypto-Solver-Skill 快速参考卡片

## 🚀 一分钟启动

```bash
# 1. 验证环境
python3 setup.py

# 2. 启动 Claude Code
npm install -g claude
claude

# 3. 输入题目
# 我有一道密码学题目...
```

---

## 📋 Claude Code 中的命令

### 基础命令

```
/skill analyze-crypto <file>          # 分析密码系统
/skill generate-attack <type>         # 生成攻击代码
/skill run-sage                       # 执行 SageMath
/skill solve-challenge <file>         # 一键求解
```

### 攻击类型

```
/skill generate-attack "low-exponent"
/skill generate-attack "common-modulus"
/skill generate-attack "fermat-factorization"
/skill generate-attack "pohlig-hellman"
/skill generate-attack "smart-attack"
/skill generate-attack "padding-oracle"
```

---

## 🔍 RSA 快速诊断

### 我看到 e=3？

→ 尝试: 低加密指数攻击  
✅ 代码模板: `templates/attack-templates/low-exponent-attack.py`

### 我看到多个公钥 (e1, e2) 和相同 n？

→ 尝试: 公共模数攻击  
✅ 代码模板: `templates/attack-templates/common-modulus-attack.py`

### 我看到 p 和 q 接近？

→ 尝试: Fermat 分解  
✅ 代码模板: `templates/attack-templates/fermat-factorization.py`

### 我看到 e 非常大，d 可能很小？

→ 尝试: Wiener 攻击  
⚠️ 框架在 `prompt.md` 中有详细说明

---

## 🔐 ECC 快速诊断

### 曲线阶有小素因子？

→ 尝试: Pohlig-Hellman 攻击

### j-invariant 特殊 (0 或 1728)？

→ 尝试: Smart 攻击（p-adic lifting）

### 题目允许有无效点？

→ 尝试: Invalid Curve Attack

---

## 📊 工作流检查清单

```
[ ] 系统分析
    [ ] 计算法和参数已识别
    [ ] 流程图已画出
    [ ] 公开/私密参数明确

[ ] 漏洞识别
    [ ] 至少找到一个可利用的漏洞
    [ ] 漏洞的数学原理理解
    [ ] 等待 AI 确认

[ ] 攻击策略
    [ ] 具体的步骤明确
    [ ] 数学推导就绪
    [ ] 复杂度评估完成
    [ ] 等待用户启动实施

[ ] 代码生成与执行
    [ ] 代码已生成
    [ ] 测试通过
    [ ] Flag 已获取

[ ] 文档生成
    [ ] analyse.md 已生成
    [ ] 数学公式完整
    [ ] 代码和输出已包含
```

---

## 🛠️ SageMath 常用命令

```sage
# 因子分解
factor(12345)           # 整数分解
factor(x^3 - 8)         # 多项式分解

# 模运算
inverse_mod(a, n)       # 模逆元
gcd(a, b)              # 最大公约数
lcm(a, b)              # 最小公倍数

# 格论
Matrix([[1,2],[3,4]]).LLL()   # LLL 约简
Matrix([[1,2],[3,4]]).BKZ()   # BKZ 约简

# 椭圆曲线
E = EllipticCurve([a, b])          # 定义曲线 y^2 = x^3 + ax + b
P = E(x, y)                        # 定义点
discrete_log(Q, P)                 # 离散对数

# 数论
is_prime(n)            # 素性测试
next_prime(n)          # 下一个素数
factor_ecm(n)          # ECM 分解
```

---

## 📁 项目文件快速查询

| 需要什么       | 位置                          |
| -------------- | ----------------------------- |
| 知识库和决策表 | `prompt.md`                   |
| 运行配置       | `config.toml`                 |
| Python 工具    | `tools/`                      |
| Sage 执行器    | `tools/sage-executor.py`      |
| 密码学工具库   | `tools/crypto-utils.py`       |
| RSA 攻击模板   | `templates/attack-templates/` |
| 完整文档       | `README.md`                   |
| 安装指南       | `SETUP_GUIDE.md`              |
| 环境检测       | `setup.py`                    |

---

## ⏱️ 时间预期

| 任务                 | 时间     |
| -------------------- | -------- |
| 系统分析             | 2-5 min  |
| 漏洞识别             | 3-10 min |
| 攻击策略             | 5-10 min |
| 代码生成             | 2-3 min  |
| 小规模 Exploit       | < 1 min  |
| 格规约（大 n）       | 1-5 min  |
| 因子分解（1024-bit） | 1-10 min |
| 离散对数（小阶）     | < 1 min  |

---

## 🔄 常见工作流示例

### 流程 1: RSA 低指数

```
题目输入
  ↓
识别 e=3
  ↓
使用 gmpy2.iroot()
  ↓
✓ Flag
```

### 流程 2: ECC Pohlig-Hellman

```
题目输入
  ↓
分解曲线阶
  ↓
发现小素因子
  ↓
子群离散对数求解
  ↓
CRT 合并
  ↓
✓ Flag
```

### 流程 3: 格密码

```
题目输入
  ↓
构造格矩阵
  ↓
LLL/BKZ 约简
  ↓
提取最短向量
  ↓
✓ Flag
```

---

## 🐛 5 个最常见的问题和解决方案

### 问题 1: "sage: command not found"

```bash
wsl sage --version  # 检查 WSL
wsl sudo apt install sagemath  # 安装
```

### 问题 2: "gmpy2 import error"

```bash
pip install gmpy2 -U
# 或从源编译
pip install gmpy2 --no-binary gmpy2
```

### 问题 3: "超时错误"

解决方案：

1. 减少迭代次数
2. 使用更快的算法
3. 增加超时时间 (`config.toml` 中的 `timeout`)

### 问题 4: "权限拒绝"

```bash
chmod +x tools/sage-executor.py
chmod +x setup.py
```

### 问题 5: "我的 Flag 不对"

检查清单：

- [ ] 密文格式是否正确？
- [ ] 数据转换（hex → bytes） 是否正确？
- [ ] 攻击是否真的找到了明文？
- [ ] Flag 格式是否需要特定转换？

---

## 📱 快速查询表

### Python Package 导入

```python
from gmpy2 import iroot              # 高精度 n 次方根
from sympy import factorint, crt     # 因子分解和 CRT
from pwntools import *               # 远程交互 (动态题)
import numpy as np                   # 数值计算
```

### 数学操作速查

```python
# 模逆元
pow(a, -1, m)              # Python 3.8+
inverse_mod(a, m)  # SageMath

# 中国剩余定理
# 手写实现见 tools/crypto-utils.py

# 扩展欧几里得
from tools.crypto_utils import egcd

# Fermat 分解
from templates.attack_templates.fermat_factorization import fermat_factorization
```

### SageMath Shell 速查

```
sage: n = 12345
sage: factor(n)
sage: E = EllipticCurve([1, 2])
sage: P = E(0, 0)
sage: P.order()
```

---

## 🎯 优化技巧

**加快 SageMath 执行**:

```bash
export SAGE_NUM_THREADS=4
wsl sage -c "..."
```

**并行求解多个小问题**:

```python
# 使用 multiprocessing
import multiprocessing
```

**减少内存占用**:

```python
# 不要加载整个 SageMath，只用 sympy
from sympy import factor
```

---

## 📞 当你卡住时

### 第 1 步: 查看知识库

```
查看 prompt.md 的相关决策表
```

### 第 2 步: 查看代码示例

```
templates/attack-templates/ 中查找类似的攻击
```

### 第 3 步: 运行 setup.py

```bash
python3 setup.py
# 诊断环境问题
```

### 第 4 步: 查看 SETUP_GUIDE.md

```
获取常见问题和故障排除
```

### 第 5 步: 求助

- GitHub Issues
- Claude Code 讨论频道
- 密码学社区 (Cryptohack)

---

## ✨ 高级技巧

### 技巧 1: 调试 SageMath 代码

```sage
# 创建 test.sage
# 直接运行
wsl sage test.sage

# 或交互式
wsl sage
sage: # 输入代码
```

### 技巧 2: 集成 FactorDB

```python
import requests

def factordb(n):
    response = requests.get(f"http://factordb.com/api?n={n}")
    factors = response.json()
    return factors['factors']
```

### 技巧 3: 远程 Oracle 交互

```python
from pwntools import remote

r = remote('challenge.server.com', 1337)
r.sendline(payload)
response = r.recvline()
```

### 技巧 4: 性能基准测试

```python
import time

start = time.time()
result = factorize_large_number(n)
elapsed = time.time() - start
print(f"耗时: {elapsed:.2f}s")
```

---

## 🎓 学习路径

**初级** (快速学习):

1. 阅读 README.md 理解基本概念
2. 运行 setup.py 检视环境
3. 尝试一个 low-exponent 题目

**中级** (深入理解):

1. 学习 prompt.md 中的数学原理
2. 理解 tools/crypto-utils.py 代码
3. 尝试多种 RSA 攻击

**高级** (自己写攻击):

1. 阅读密码学论文
2. 自己实现新的攻击
3. 贡献到项目中

---

## 🎉 成功的 Flag 获取流程

```
输入题目
  ↓
启动分析...
  ↓
[系统分析] ✓ 识别 RSA (e=3)
  ↓
[漏洞识别] ✓ 低指数攻击可行
  ↓
⏸️  等待确认...
  ↓
[攻击策略] ✓ 直接求立方根
  ↓
⏸️  等待启动...
  ↓
[代码实现] ✓ 生成 exploit.py
  ↓
[执行] ✓ 运行测试
  ↓
[结果] 🚀 Flag: flag{...}
  ↓
[文档] 📄 analyse.md 已生成
```

---

**最后提醒**: 始终检查你的数学和代码逻辑。不要盲目信任工具！🎓

_Version: 1.0.0 | Last Updated: 2026-02-06_
