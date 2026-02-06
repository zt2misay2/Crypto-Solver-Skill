#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA 公共模数攻击 (Common Modulus Attack) 模板
适用于: 多个公钥共享相同的模数 n
"""

import math
from typing import Tuple, Optional

def common_modulus_attack(
    n: int,
    e1: int, 
    e2: int,
    c1: int,
    c2: int
) -> Optional[int]:
    """
    公共模数攻击
    
    给定:
    - 同一消息 m 被加密两次: c1 = m^e1 mod n, c2 = m^e2 mod n
    - 相同模数 n
    
    如果 gcd(e1, e2) = 1，可以恢复 m
    
    原理:
    由欧几里得算法，存在整数 x, y 使得: e1*x + e2*y = 1
    则: m = c1^x * c2^y mod n
    
    Args:
        n: RSA 模数
        e1, e2: 两个公钥指数
        c1, c2: 对应的密文
    
    Returns:
        明文 m，若不存在则返回 None
    """
    
    # === 步骤 1: 检查 gcd(e1, e2) ===
    gcd_e = math.gcd(e1, e2)
    
    if gcd_e != 1:
        print(f"[!] gcd({e1}, {e2}) = {gcd_e} != 1")
        print(f"    无法应用此攻击")
        return None
    
    # === 步骤 2: 扩展欧几里得算法求 x, y ===
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """返回 (gcd, x, y) 使得 a*x + b*y = gcd"""
        if a == 0:
            return (b, 0, 1)
        
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return (gcd_val, x, y)
    
    _, x, y = extended_gcd(e1, e2)
    
    print(f"[+] 扩展欧几里得算法结果:")
    print(f"    {e1} * {x} + {e2} * {y} = 1")
    
    # === 步骤 3: 计算 m = c1^x * c2^y mod n ===
    
    # 处理负指数
    if x < 0:
        # c1^x = (c1^(-1))^(-x)
        c1_inv = pow(c1, -1, n)  # Python 3.8+
        m = pow(c1_inv, -x, n)
    else:
        m = pow(c1, x, n)
    
    if y < 0:
        # c2^y = (c2^(-1))^(-y)
        c2_inv = pow(c2, -1, n)
        m = (m * pow(c2_inv, -y, n)) % n
    else:
        m = (m * pow(c2, y, n)) % n
    
    print(f"[+] 计算明文: m = {c1}^{x} * {c2}^{y} mod {n}")
    print(f"    m = {m}")
    
    # === 步骤 4: 验证 ===
    verify_c1 = pow(m, e1, n)
    verify_c2 = pow(m, e2, n)
    
    if verify_c1 == c1 and verify_c2 == c2:
        print(f"[✓] 验证成功!")
        print(f"    m^{e1} mod n = {verify_c1} (expected {c1})")
        print(f"    m^{e2} mod n = {verify_c2} (expected {c2})")
        return m
    else:
        print(f"[!] 验证失败")
        return None


def common_modulus_multiple(
    n: int,
    enc_pairs: list  # [(e1, c1), (e2, c2), ...]
) -> Optional[int]:
    """
    多个密文的公共模数攻击
    
    Args:
        n: RSA 模数
        enc_pairs: [(e1, c1), (e2, c2), ...]
    
    Returns:
        明文 m
    """
    
    if len(enc_pairs) < 2:
        return None
    
    # 逐对进行攻击，逐步恢复明文线性组合
    e1, c1 = enc_pairs[0]
    
    for i in range(1, len(enc_pairs)):
        e2, c2 = enc_pairs[i]
        result = common_modulus_attack(n, e1, e2, c1, c2)
        
        if result is None:
            return None
        
        # 更新用于下一轮
        # 这里的逻辑可能需要调整，取决于具体场景
        c1 = result
        e1 = 1  # 下一轮的 e1 是 1（因为已恢复明文）
    
    return c1


def gcd_modulus_factorization(n1: int, n2: int) -> Optional[Tuple[int, int]]:
    """
    通过 GCD 分解两个 RSA 模数
    
    如果两个 RSA 模数共享公因子 p:
    n1 = p * q1
    n2 = p * q2
    
    则 gcd(n1, n2) = p
    
    Args:
        n1, n2: 两个 RSA 模数
    
    Returns:
        (p, q) 其中 p 是公因子，或 None
    """
    
    p = math.gcd(n1, n2)
    
    if p == 1:
        print(f"[!] gcd({n1}, {n2}) = 1, 无共享因子")
        return None
    
    print(f"[+] 找到公因子: p = {p}")
    
    # 分解第一个模数
    q = n1 // p
    
    print(f"    n1 = {n1} = {p} * {q}")
    print(f"    验证: {p} * {q} = {p * q}")
    
    return (p, q)


# ============= 使用示例 =============

if __name__ == "__main__":
    print("[*] RSA 公共模数攻击演示\n")
    
    # 示例数据
    n = 10007 * 10009  # n = 100170063
    
    # 两个不同的 e
    e1 = 3
    e2 = 7
    
    # 消息
    m = 12345
    
    # 加密
    c1 = pow(m, e1, n)
    c2 = pow(m, e2, n)
    
    print(f"模数 n = {n}")
    print(f"消息 m = {m}")
    print(f"密密文 1: c1 = m^{e1} mod n = {c1}")
    print(f"密密文 2: c2 = m^{e2} mod n = {c2}")
    print()
    
    # 进行攻击
    recovered_m = common_modulus_attack(n, e1, e2, c1, c2)
    
    if recovered_m == m:
        print(f"\n[✓✓✓] 成功恢复明文: {recovered_m}")
    else:
        print(f"\n[×] 恢复失败")
