# continually add and show the sum of floating points
def get_money():
    sum = 0
    while True:
        x = input()
        print()
        if x == "q":
            break

        sum += float(x)
        str = "sum: {0}".format(sum)
        print(str)

    return sum

sum = get_money()
print("sum: {0}".format(sum))
