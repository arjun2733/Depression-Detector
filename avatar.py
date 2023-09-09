import python_avatars as pa
import random 
import sys
# Completely random avatar
dict = {}


def generate_key():
    key = random.randint(0,sys.maxsize)
    if key not in dict.keys():
        return key 
    else :
        generate_key() 

def random_avatar():

    random_avatar_1 = pa.Avatar.random()
    print(random_avatar_1)
    random_avatar_1.render("my_avatar.svg")
    key = generate_key()
    dict[key] = random_avatar_1

generate_again=1
while(generate_again==1):
    random_avatar()
    dict_keys = list(dict.keys())
    print(dict_keys)
    print(dict[dict_keys[0]])
    print(dict)
    generate_again=int(input("\nenter 1 for yes and 0 for no: "))
