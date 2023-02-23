stringA = "[Mon, sun, Tue, wed]"
# Given string
print("Given string", stringA)
print(type(stringA))
# String to list
res = stringA.strip('][').split(',' or ', ')
# Result and its type
print("final list", res)
print(type(res))