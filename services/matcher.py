def compatibility(u1, u2):
    if u1.city != u2.city:
        return 0

    score = 0
    if u1.food == u2.food: score += 15
    if u1.sleep == u2.sleep: score += 15
    if u1.smoking == u2.smoking: score += 20
    if u1.drinking == u2.drinking: score += 10
    if u1.cleanliness == u2.cleanliness: score += 15
    if u1.occupation == u2.occupation: score += 10
    if u1.timing == u2.timing: score += 15

    return score
