def solve():
    recipes = []
    potentials = {}

    for line in open("day-21-input.txt").readlines():
        split = line.split(" (contains ")
        ingredients = split[0].split(" ")
        allergens = split[1].strip()[0:-1].split(", ")

        recipes.append((ingredients, allergens))

        for ingredient in ingredients:
            if ingredient not in potentials:
                potentials[ingredient] = set()
            for allergen in allergens:
                potentials[ingredient].add(allergen)

    for i in range(0, len(recipes) - 1):
        for j in range(i + 1, len(recipes)):
            shared_allergens = [allergen for allergen in recipes[i][1] if allergen in recipes[j][1]]
            not_shared_ingredients = [ingredient
                                      for ingredient in recipes[i][0] + recipes[j][0] if
                                      ingredient not in recipes[i][0] or ingredient not in
                                      recipes[j][0]]

            for ingredient in not_shared_ingredients:
                for allergen in shared_allergens:
                    potentials[ingredient].discard(allergen)

    safe_ingredients = [ingredient for ingredient, allergens in potentials.items() if len(allergens) == 0]

    count = 0
    for ingredients, _ in recipes:
        for safe_ingredient in safe_ingredients:
            if safe_ingredient in ingredients:
                count += 1
    print(f"Part one = {count}")

    working = {}
    for ingredient in potentials:
        if ingredient not in safe_ingredients:
            working[ingredient] = potentials[ingredient]

    allergens = set()
    for (_, a) in recipes:
        for allergen in a:
            allergens.add(allergen)

    dangerous_ingredients = {}
    while len(working) > 0:
        for working_ingredient, working_allergens in working.items():
            if len(working_allergens) == 1:
                w = working_ingredient
                break
        dangerous_ingredients[w] = next(iter(working[w]))
        working.pop(w)
        for a, b in working.items():
            b.discard(dangerous_ingredients[w])

    sorted_dangerous_ingredients = list(dangerous_ingredients.items())
    sorted_dangerous_ingredients.sort(key=lambda x: x[1])
    part_two = ",".join([p[0] for p in sorted_dangerous_ingredients])
    print(f"Part two = {part_two}")


solve()
