import json
import random
import string

def generate_large_data(num_records=100000):
    """Generates a large JSON file with random data"""
    data = []
    for _ in range(num_records):
        record = {
            "id": random.randint(1, 1000000),
            "name": ''.join(random.choices(string.ascii_letters, k=10)),
            "value": random.uniform(1.0, 1000.0),
            "category": random.choice(["A", "B", "C", "D"])
        }
        data.append(record)
    
    with open("data.json", "w") as f:
        json.dump(data, f)

    print("Large data.json generated.")

if __name__ == "__main__":
    generate_large_data()
