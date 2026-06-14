inventory= {
"chips" : 3,
"juice" : 19,
"biscuits": 32,
}
for item, stock in inventory.items():
    if stock<5:
        print(f"ALERT:stock for {item} is low, only {stock} left")
