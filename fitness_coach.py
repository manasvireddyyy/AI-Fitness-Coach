import os

print("===== AI FITNESS COACH =====")
print("1. Squat Counter")
print("2. Push-Up Counter")
print("3. Skipping Counter")
print("4. Exit")

choice = input("Select option: ")

if choice == "1":
    os.system("python3 main.py")
elif choice == "2":
    os.system("python3 pushup.py")
elif choice == "3":
    os.system("python3 skipping.py")
elif choice == "4":
    exit()
else:
    print("Invalid choice. Please select again.")