from Kernel import Kernel

kernel = Kernel()
kernel.learn("chat_app/std-startup.xml")
kernel.respond("load aiml")

kernel.respond("Hi")
kernel.learn("std-startup.xml")
# while True:
#     print kernel.respond(raw_input("> "))

# while True:
#     print kernel.respond("")

def askquestion(stringinput):
	kernel.learn("std-startup.xml")
	return kernel.respond(stringinput)