simple_list = [1, 2, 3, 4]

simple_list.extend([5, 6, 7, 8])
print(simple_list)

del (simple_list[0])
print(simple_list)

d = {'name': 'Max'}
print(d.items())
# -> dict_items([('name', 'Max')])

for k, v in d.items():
    print(k, v)
    # -> name Max

del (d['name'])
print(d)
# -> {}

t = (1, 2, 3)
print(t.index(3))
# -> 2

# del (t[0])
# print(t)  # Error -> Tuple is NOT Mutable

set = {'Max', 'Anna', 'Max'}

set.remove('Max')
set.discard('Max')
# -> {'Anna'}

print(set)
