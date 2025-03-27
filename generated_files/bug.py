def calculate_average(numbers):
    total = sum(numbers)
    avg = total / len(numbers) 
    return avg

print("The average is: " + str(calculate_average(numbers)))
numbers = [10, 20, 30, 40, 50]
print("The average is: " + calculate_average(numbers)) 