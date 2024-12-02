def sqrt_newton_recursive(x, guess=None, tolerance=1e-10):
    if guess is None:
        guess = x / 2.0  # 初始猜测值

    new_guess = 0.5 * (guess + x / guess)

    # 如果新的猜测值与旧的猜测值之差小于容差，则返回新的猜测值
    if abs(new_guess - guess) < tolerance:
        return new_guess

    # 否则，递归调用自身
    return sqrt_newton_recursive(x, new_guess, tolerance)

# 求解 sqrt(2)
result = sqrt_newton_recursive(2)
print(result)
