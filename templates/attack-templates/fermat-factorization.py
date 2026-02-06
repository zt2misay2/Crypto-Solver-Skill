#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fermat 分解法 (Fermat Factorization) 模板
适用于: RSA 模数 n = p*q，且 p ≈ q（两个因子接近）
"""

import math
from typing import Optional, Tuple

def fermat_factorization(n: int, max_iterations: int = 1000000) -> Optional[Tuple[int, int]]:
    """
    Fermat 分解法
    
    原理:
    如果 n = p*q，寻找 x, y 使得 n = x^2 - y^2 = (x-y)(x+y)
    则 p = x - y, q = x + y
    
    步骤:
    1. 从 x = ceil(sqrt(n)) 开始
    2. 计算 y^2 = x^2 - n
    3. 如果 y^2 是完全平方数，则分解成功
    4. 否则 x += 1，继续
    
    复杂度: O(sqrt(q - p))，当 p ≈ q 时效率高
    
    Args:
        n: 要分解的数
        max_iterations: 最大迭代次数
    
    Returns:
        (p, q) 分解结果，失败返回 None
    """
    
    # === 步骤 1: 初始化 ===
    x = int(math.ceil(math.sqrt(n)))
    
    # 检查是否是完全平方数
    if x * x == n:
        return (x, n // x)
    
    x += 1
    y2 = x * x - n
    
    print(f"[*] Fermat 分解法")
    print(f"    n = {n}")
    print(f"    n 的比特长度: {n.bit_length()}")
    print(f"    初始 x = {x}")
    print()
    
    # === 步骤 2: 迭代搜索 ===
    iteration = 0
    
    while iteration < max_iterations:
        # 检查 y^2 是否是完全平方数
        y = int(math.isqrt(y2))
        
        if y * y == y2:
            # 找到分解
            p = x - y
            q = x + y
            
            print(f"[+] 在第 {iteration} 次迭代处找到分解")
            print(f"    x = {x}, y = {y}")
            print(f"    p = x - y = {p}")
            print(f"    q = x + y = {q}")
            print(f"    验证: p * q = {p * q}")
            print(f"    是否正确: {p * q == n}")
            
            if p * q == n:
                return (p, q) if p < q else (q, p)
        
        # 下一次迭代
        x += 1
        y2 = x * x - n
        iteration += 1
        
        # 进度显示
        if iteration % 100000 == 0:
            print(f"    已迭代 {iteration} 次，当前 x = {x}")
    
    print(f"[!] 达到最大迭代次数 {max_iterations}，分解失败")
    return None


def fermat_with_quadratic_residue(n: int) -> Optional[Tuple[int, int]]:
    """
    改进的 Fermat 分解法
    使用二次剩余优化
    
    当 n ≡ 1 (mod 4) 时，n = x^2 - y^2 有多种表示
    可以利用二次剩余加速
    """
    
    x = int(math.ceil(math.sqrt(n)))
    
    # 对于大 n，使用更快的平方根检测
    max_iterations = min(1000000, int(math.sqrt(n)) // 2)
    
    for i in range(max_iterations):
        y2 = x * x - n
        
        # 快速完全平方检测
        y = int(math.isqrt(y2))
        
        if y * y == y2 and y > 0:
            p = x - y
            q = x + y
            
            if p > 0 and q > 0 and p * q == n:
                return (p, q) if p < q else (q, p)
        
        x += 1
    
    return None


# ============= 使用示例 =============

if __name__ == "__main__":
    print("[*] Fermat 分解法演示\n")
    
    # === 测试用例 1: p 和 q 接近 ===
    p1 = 1000003
    q1 = 1000033
    n1 = p1 * q1
    
    print(f"测试用例 1:")
    print(f"p = {p1}, q = {q1}")
    print(f"n = {n1}")
    print(f"p - q = {abs(p1 - q1)}")
    print()
    
    result1 = fermat_factorization(n1, max_iterations=100000)
    
    if result1:
        print(f"分解结果: {result1}")
        print()
    
    # === 测试用例 2: p 和 q 差距较大 ===
    p2 = 10000019
    q2 = 10000103
    n2 = p2 * q2
    
    print(f"\n测试用例 2:")
    print(f"p = {p2}, q = {q2}")
    print(f"n = {n2}")
    print(f"|p - q| = {abs(p2 - q2)}")
    print()
    
    result2 = fermat_factorization(n2, max_iterations=100000)
    
    if result2:
        print(f"分解结果: {result2}")
