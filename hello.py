def digit_sum(n):
    """计算一个数的各位数字之和"""
    total = 0
    while n > 0:
        total += n % 10
        n = n // 10
    return total

def find_digit_sum_numbers(limit, target_sum):
    """找出指定范围内各位数字之和等于目标值的所有数字"""
    result = []
    for num in range(1, limit + 1):
        if digit_sum(num) == target_sum:
            result.append(num)
    return result

# 找出1000以内各位数之和为10的数字
limit = 1000
target_sum = 10
numbers = find_digit_sum_numbers(limit, target_sum)

# 输出结果
print(f"1000以内各位数之和为{target_sum}的数字共有 {len(numbers)} 个：")
print(numbers)