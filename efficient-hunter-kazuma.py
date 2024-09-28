import json

# Take JSON data as input from the user
data = input("Enter the JSON data: ")

# Parse the JSON data
parsed_data = json.loads(data)

# Access the array under "monsters"
monsters_array = parsed_data[0]["monsters"]

print(monsters_array)

# Example function that processes the monsters array
def process_monsters(monsters):
    # Example: Calculate the sum of the monsters array
    return sum(monsters)

# Process the monsters array
result = process_monsters(monsters_array)

print("Processed result:", result)
