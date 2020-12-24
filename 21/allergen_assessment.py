from typing import List, Tuple, Set, Dict

Ingredient = str
Allergen = str
Food = Tuple[Set[Ingredient], Set[Allergen]]


def load_foods(path: str) -> List[Food]:
    f = open(path)
    foods = []
    for line in f:
        words = line.split()
        ing = set()
        al = set()
        i = 0
        while i < len(words) and words[i] != '(contains':
            ing.add(words[i])
            i += 1
        i += 1
        while i < len(words):
            al.add(words[i][:-1])
            i += 1
        foods.append((ing, al))
    return foods


def get_allergens(foods: List[Food]) -> Set[Allergen]:
    allergens = set()
    for ing, al in foods:
        allergens.update(al)
    return allergens


def get_ingredients(foods: List[Food]) -> Set[Ingredient]:
    ingredients = set()
    for ing, al in foods:
        ingredients.update(ing)
    return ingredients


def contains_allergen(food: Food, allergen: Allergen) -> bool:
    return allergen in food[1]


def contains_ingredient(food: Food, ingredient: Ingredient) -> bool:
    return ingredient in food[0]


def get_foods_by_allergens(foods: List[Food], allergen: Allergen) -> List[Food]:
    result = []
    for i in range(len(foods)):
        if contains_allergen(foods[i], allergen):
            result.append(foods[i])
    return result


def get_foods_by_ingredient(foods: List[Food], ingredient: Ingredient) -> List[Food]:
    result = []
    for i in range(len(foods)):
        if contains_ingredient(foods[i], ingredient):
            result.append(foods[i])
    return result


def common_ingredients(foods: List[Food]) -> Set[Ingredient]:
    c_ing = set(foods[0][0])
    for ing, al in foods:
        c_ing.intersection_update(ing)
    return c_ing


def remove_ingredient(alergens: List[Tuple[Allergen, Set[Ingredient]]],
                      ingredient: Ingredient) -> None:
    for al, ing in alergens:
        try:
            ing.remove(ingredient)
        except KeyError:
            pass


def solve(file_path: str, name: str):
    print()
    print(name)

    foods = load_foods(file_path)
    allergens = get_allergens(foods)

    # becomes ingredients without allergens
    ingredients = get_ingredients(foods)

    tmp_allergens = []

    for al in allergens:
        f = get_foods_by_allergens(foods, al)
        c_ing = common_ingredients(f)
        # store common ingredients - they may be allergens
        tmp_allergens.append((al, c_ing))
        # remove them from ingredients
        ingredients.difference_update(c_ing)

    # count nonalergen ingredients
    counter = 0
    for ing in ingredients:
        counter += len(get_foods_by_ingredient(foods, ing))
    print('Nonalergen ingredients count:', counter)

    # translate allergens
    allergen_list = []
    while len(tmp_allergens) > 0:
        for al, ing_set in tmp_allergens:
            if len(ing_set) == 1:
                tmp_allergens.remove((al, ing_set))
                ing = ing_set.pop()
                remove_ingredient(tmp_allergens, ing)
                allergen_list.append((al, ing))
    allergen_list.sort()

    # print translated allergens
    print('Dangerous ingredient list: "', end='')
    print(allergen_list[0][1], end='')
    for i in range(1, len(allergen_list)):
        print(',', allergen_list[i][1], sep='', end='')
    print('"')


if __name__ == '__main__':
    solve('21/test_input.txt', 'Test')
    solve('21/input.txt', 'Task')
