house1= {
"neighbourhood" : "DHA",
"price" : 50000000,
"bedrooms" : 3,
}
house2= {
"neighbourhood" : "PECHS",
"price" : 20000000,
"bedrooms" : 2,
}
house3= {
"neighbourhood" : "Malir",
"price" : 450000000,
"bedrooms" : 4,
}
properties = [house1, house2, house3]  
choice = input("house no/:" )
if choice=='1':
    print(f"this house is in {house1["neighbourhood"]}, has {house1["bedrooms"]} bedrooms and is for {house1["price"]}")
elif choice=='2':
    print(f"this house is in {house2["neighbourhood"]}, has {house2["bedrooms"]} bedrooms and is for {house2["price"]}")
else:
    print(f"this house is in {house3["neighbourhood"]}, has {house3["bedrooms"]} bedrooms and is for {house3["price"]}")


