
import string

with open('input/1.txt') as f:
    text = f.read().strip()


print([(i,a) for i,a in enumerate(text.splitlines()) if not a.strip(string.ascii_letters)])
print(sum([int(a.strip(string.ascii_letters)[0] + a.strip(string.ascii_letters)[-1]) for a in text.splitlines()]))



text = text.replace("nine", "nine9nine")
text = text.replace("eight", "eight8eight")
text = text.replace("one", "one1one")
text = text.replace("two", "two2two")
text = text.replace("four", "four4four")
text = text.replace("five", "five5five")
text = text.replace("six", "six6six")
text = text.replace("seven", "seven7seven")
text = text.replace("three", "three3three")
print(sum([int(a.strip(string.ascii_letters)[0] + a.strip(string.ascii_letters)[-1]) for a in text.splitlines()]))
