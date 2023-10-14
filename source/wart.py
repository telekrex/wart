import os


def filetree():
	for file in os.listdir('../story'):
		print(file)


filetree()


# def main():
# 	while True:
# 		action = input("")