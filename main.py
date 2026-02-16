from system_core import PrioritySoundSystem

print("PrioritySound System")
print("---------------------")
print("Use UP arrow to increase sensitivity")
print("Use DOWN arrow to decrease sensitivity")
print("Press 'f' to mark false alert")

name = input("Enter your name: ")

system = PrioritySoundSystem(name)
system.run()
