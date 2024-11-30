def prime(max_limit: int):
    if max_limit < 2:
        return []

    is_prime = [True] * (max_limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(max_limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, max_limit + 1, i):
                is_prime[j] = False

    return [num for num, prime in enumerate(is_prime) if prime]





