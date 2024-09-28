import json

# data = input("Input: ")

data = json.dumps([
    {
      "monsters": [1,4,5,0,4]
    }
])
parsed_data = json.loads(data)
monsters_array = parsed_data[0]["monsters"]

# MAIN
def main(monsters):
    # Example: Calculate the sum of the monsters array
    return sum(monsters)

# Process the monsters array
efficiency = main(monsters_array)

# Output the efficiency
output_data = json.dumps([
    {
      "efficiency": efficiency
    }
])
print(output_data)