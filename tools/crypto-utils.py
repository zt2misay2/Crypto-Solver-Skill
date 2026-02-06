#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码学工具库
提供常用的密码学分析和数学工具
"""

import os
from typing import Tuple, List, Optional
from math import gcd, isqrt

class CryptoAnalyzer:
    """密码学分析工具"""
    
    @staticmethod
    def analyze_rsa_modulus(n: int) -> dict:
        """
        分析 RSA 模数
        
        Args:
            n: RSA 模数
        
        Returns:
            分析结果
        """
        
        analysis = {
            "n": n,
            "bit_length": n.bit_length(),
            "is_prime": is_probable_prime(n),
            "small_factors": find_small_factors(n, limit=1000),
        }
        
        return analysis
    
    @staticmethod
    def gcd_factorize(n1: int, n2: int) -> Optional[int]:
        """
        通过 GCD 分解两个模数
        
        Args:
            n1: 第一个模数
            n2: 第二个模数
        
        Returns:
            公因子（如果找到），否则 None
        """
        
        factor = gcd(n1, n2)
        
        if factor == 1:
            return None
        
        return factor
    
    @staticmethod
    def fermat_factorization(n: int, max_iter: int = 100000) -> Optional[Tuple[int, int]]:
        """
        Fermat 分解法
        适用于 p 和 q 接近的情况
        
        Args:
            n: 要分解的数
            max_iter: 最大迭代次数
        
        Returns:
            (p, q) 或 None
        """
        
        x = isqrt(n)
        if x * x == n:
            return (x, x)
        
        x += 1
        y2 = x * x - n
        
        for _ in range(max_iter):
            y = isqrt(y2)
            
            if y * y == y2:
                p = x - y
                q = x + y
                
                if p * q == n:
                    return (p, q) if p < q else (q, p)
            
            x += 1
            y2 = x * x - n
        
        return None


def is_probable_prime(n: int, k: int = 40) -> bool:
    """
    Miller-Rabin 素性测试
    
    Args:
        n: 要测试的数
        k: 测试轮次
    
    Returns:
        是否可能是素数
    """
    
    if n < 2:
        return False
    
    if n == 2 or n == 3:
        return True
    
    if n % 2 == 0:
        return False
    
    # 写成 n-1 = d * 2^r 的形式
    r = 0
    d = n - 1
    
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # 进行 k 轮测试
    for _ in range(k):
        a = 2 + os.urandom(1)[0] % (n - 4)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            
            if x == n - 1:
                break
        else:
            return False
    
    return True


def find_small_factors(n: int, limit: int = 1000) -> List[int]:
    """
    寻找小的因子
    
    Args:
        n: 要分解的数
        limit: 素数限制
    
    Returns:
        小因子列表
    """
    
    factors = []
    
    # 尝试小素数
    for p in range(2, min(limit, int(n**0.5) + 1)):
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
    
    return factors


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    扩展欧几里得算法
    
    Returns:
        (gcd, x, y) 使得 a*x + b*y = gcd
    """
    
    if a == 0:
        return (b, 0, 1)
    
    gcd_val, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return (gcd_val, x, y)


def modinv(a: int, m: int) -> int:
    """
    模逆元计算
    
    Args:
        a: 底数
        m: 模数
    
    Returns:
        a 模 m 的逆元
    """
    
    gcd_val, x, _ = egcd(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"模逆元不存在: gcd({a}, {m}) = {gcd_val}")
    
    return x % m


def chinese_remainder_theorem(congruences: List[Tuple[int, int]]) -> int:
    """
    中国剩余定理
    
    Args:
        congruences: [(a1, m1), (a2, m2), ...] 形式的同余方程
    
    Returns:
        满足所有同余方程的 x
    """
    
    if not congruences:
        return 0
    
    a, m = congruences[0]
    
    for a_i, m_i in congruences[1:]:
        gcd_val, p, q = egcd(m, m_i)
        
        if (a_i - a) % gcd_val != 0:
            raise ValueError("无解")
        
        lcm = m * m_i // gcd_val
        a = (a + m * ((a_i - a) // gcd_val) * p) % lcm
        m = lcm
    
    return a % m
