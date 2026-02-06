#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA 低加密指数攻击 (Low Exponent Attack) 模板
适用于: e = 3 或 e 很小，且消息不重复加密的情况
"""

def low_exponent_attack(e: int, c: int) -> int:
    """
    低加密指数攻击
    
    当 e 很小且 m^e < n 时，c = m^e（不需要模 n）
    直接求 e 次方根即可获得明文
    
    Args:
        e: 公钥指数
        c: 密文
    
    Returns:
        明文 m
    """
    
    try:
        from gmpy2 import iroot
    except ImportError:
        print("[!] 需要安装 gmpy2: pip install gmpy2")
        return None
    
    # === 方法 1: 使用 gmpy2 (推荐) ===
    m, is_perfect = iroot(c, e)
    
    if is_perfect:
        return int(m)
    
    # === 方法 2: 使用 SageMath ===
    # 在 SageMath 中运行:
    # m = int(c^(1/e))
    
    # === 方法 3: 二分法 (纯 Python) ===
    low = 0
    high = c
    
    while low <= high:
        mid = (low + high) // 2
        mid_e = pow(mid, e)
        
        if mid_e == c:
            return mid
        elif mid_e < c:
            low = mid + 1
        else:
            high = mid - 1
    
    return None


def hastad_broadcast_attack(ciphertexts: list, moduli: list, e: int) -> str:
    """
    Håstad 广播攻击
    
    当同一消息用 e 个不同的公钥 (n_i, e) 加密时
    可以通过 CRT 恢复明文
    
    Args:
        ciphertexts: [c_1, c_2, ..., c_e]
        moduli: [n_1, n_2, ..., n_e]
        e: 公钥指数 (通常 = 3)
    
    Returns:
        明文消息
    """
    
    assert len(ciphertexts) == len(moduli) == e
    
    try:
        from gmpy2 import iroot
    except ImportError:
        print("[!] 需要安装 gmpy2")
        return None
    
    # === 步骤 1: 使用中国剩余定理合并 ===
    from sympy import crt as sympy_crt
    
    # CRT 结果: x ≡ c_i (mod n_i) for all i
    m_to_e, _ = sympy_crt(moduli, ciphertexts)
    
    # === 步骤 2: 求 e 次方根 ===
    m = int(iroot(m_to_e, e)[0])
    
    return m


# ============= 使用示例 =============

if __name__ == "__main__":
    # 例子 1: 低加密指数攻击 (e=3)
    print("[*] 低加密指数攻击演示")
    
    # 假设密文和指数
    e = 3
    c = 12345678  # 密文，来自 m^3
    
    m = low_exponent_attack(e, c)
    print(f"    e = {e}")
    print(f"    c = {c}")
    print(f"    m = {m}")
    print(f"    验证: {m}^{e} = {pow(m, e) if m else 'N/A'}")
    
    print()
    
    # 例子 2: Håstad 广播攻击
    print("[*] Håstad 广播攻击演示")
    
    # 模拟 3 个不同的 RSA 公钥加密同一消息
    # n_1, n_2, n_3
    # 都用 e = 3
    
    # (这里只是示例框架，需要真实数据)
    ciphertexts = [12345, 67890, 11111]
    moduli = [10007, 10009, 10037]
    e = 3
    
    # m = hastad_broadcast_attack(ciphertexts, moduli, e)
    # print(f"    Recovered message: {m}")
