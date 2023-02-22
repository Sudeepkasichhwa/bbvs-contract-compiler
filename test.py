# Python program to update
# JSON

key = ['candidat_id', 'name', 'image_url', 'post']
dict = {}

for i in range(4):
    name = input("enter name : ")
    dict[key[i]] = name

print(dict)