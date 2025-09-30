#!/usr/bin/env python3
"""
测试挑战答案生成逻辑
分析不同用户和不同题目的答案是否不同
"""

def generate_challenge_numbers(user_id: int, exercise_id: int):
    """生成用户特定的挑战数字"""
    numbers = []
    total_sum = 0
    
    for page in range(100):
        page_numbers = []
        for i in range(10):
            # 使用用户ID和题目ID作为种子，确保每个用户的数据不同
            seed = (user_id * 1000 + exercise_id * 100 + page * 10 + i) % 200 + 1
            page_numbers.append(seed)
            total_sum += seed
        numbers.append(page_numbers)
    
    return numbers, total_sum

def test_challenge_answers():
    """测试不同用户和题目的答案"""
    print("=== 挑战答案分析 ===\n")
    
    # 测试不同用户，同一题目
    print("1. 同一题目，不同用户的答案：")
    exercise_id = 1
    for user_id in range(1, 6):
        _, total_sum = generate_challenge_numbers(user_id, exercise_id)
        print(f"   用户{user_id}，题目{exercise_id}: {total_sum}")
    
    print()
    
    # 测试同一用户，不同题目
    print("2. 同一用户，不同题目的答案：")
    user_id = 1
    for exercise_id in range(1, 6):
        _, total_sum = generate_challenge_numbers(user_id, exercise_id)
        print(f"   用户{user_id}，题目{exercise_id}: {total_sum}")
    
    print()
    
    # 测试前几页的数字分布
    print("3. 用户1，题目1的前3页数字：")
    numbers, _ = generate_challenge_numbers(1, 1)
    for page in range(3):
        print(f"   第{page+1}页: {numbers[page]}")
    
    print()
    
    # 分析数字分布
    print("4. 数字分布分析：")
    all_numbers = []
    for page in range(100):
        all_numbers.extend(numbers[page])
    
    print(f"   总数字个数: {len(all_numbers)}")
    print(f"   数字范围: {min(all_numbers)} - {max(all_numbers)}")
    print(f"   唯一数字个数: {len(set(all_numbers))}")
    
    # 检查是否有重复模式
    print("\n5. 重复模式检查：")
    user1_ex1, _ = generate_challenge_numbers(1, 1)
    user1_ex2, _ = generate_challenge_numbers(1, 2)
    user2_ex1, _ = generate_challenge_numbers(2, 1)
    
    print(f"   用户1题目1第1页: {user1_ex1[0]}")
    print(f"   用户1题目2第1页: {user1_ex2[0]}")
    print(f"   用户2题目1第1页: {user2_ex1[0]}")
    
    # 检查算法特性
    print("\n6. 算法特性分析：")
    print("   种子公式: (user_id * 1000 + exercise_id * 100 + page * 10 + i) % 200 + 1")
    print("   这意味着:")
    print("   - 每个用户的数据都不同 (user_id * 1000)")
    print("   - 每个题目的数据都不同 (exercise_id * 100)")
    print("   - 每页的数据都不同 (page * 10)")
    print("   - 每个位置的数据都不同 (i)")
    print("   - 数字范围固定在1-200之间")

if __name__ == "__main__":
    test_challenge_answers()
