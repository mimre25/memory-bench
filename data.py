import json
data = json.dumps({
    "name": "John Doe",
    "age": 50,
    "children": [
        {
            "name": "Alice Doe",
            "age": 30,
            "children": [
                {
                    "name": "Emma Smith",
                    "age": 5,
                    "children": []
                },
                {
                    "name": "Liam Smith",
                    "age": 3,
                    "children": []
                }
            ]
        },
        {
            "name": "Bob Doe",
            "age": 28,
            "children": [
                {
                    "name": "Olivia Johnson",
                    "age": 7,
                    "children": []
                }
            ]
        },
        {
            "name": "Charlie Doe",
            "age": 25,
            "children": [
                {
                    "name": "Sophia Brown",
                    "age": 4,
                    "children": []
                },
                {
                    "name": "Mason Brown",
                    "age": 2,
                    "children": []
                }
            ]
        },
        {
            "name": "Diana Doe",
            "age": 22,
            "children": []
        }
    ] * 100000
}).encode()
