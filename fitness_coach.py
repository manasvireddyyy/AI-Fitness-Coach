import os

print("===== AI FITNESS COACH =====")
print("1. Squat Counter")
print("2. Push-Up Counter")
print("3. Exit")

choice = input("Select option: ")

if choice == "1":
    os.system("python3 main.py")
elif choice == "2":
    os.system("python3 pushup.py")
elif choice == "3":
    print("Exiting...")
    exit()
else:
    print("Invalid choice. Please select again.")