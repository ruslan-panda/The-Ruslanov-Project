import pymorphy2

number = 3
p = morph.parse("студент")[0]
print(f"{number} {p.make_agree_with_number(int(number)).word}")