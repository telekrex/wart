#!/usr/bin/env python3
from random import choice
import os



def sanitize(text):
	# remove non alpha-numeric
	# characters from the text
	for character in text:
		if character.isalnum():
			# ignore alphanumeric
			pass
		else:
			# remove non alphanumeric characters
			text = text.replace(character, '')
	# then force it to all lowercase
	# and remove trailing white space
	text = text.lower().strip()
	return text


def choose_from_links(user_choice, links):
	# look through the each link, where the list
	# of links looks like this:
	# links: [[[list of hooks], [list of moments]]]
	for link in links:
		# look through each link, where the link
		# looks like this:
		# link: [[list of hooks], [list of moments]]
		hooks = link[0]
		moments = link[1]
		# and hooks, moments look like this:
		# hooks: [list of hooks]
		# moments: [list of moments]
		for hook in hooks:
			# look through this link's hooks,
			# and if one matches the user choice,
			# we choose from the corresponding list
			# of moments from that link
			if sanitize(user_choice) == sanitize(hook):
				# we sanitize both user's input and the
				# story file contents just in case, and
				# to force them to be as close as possible
				return choice(moments)


def read(moment):
	# !
	# this function is massively ugly
	# so I'll clean it up later, for now
	# I just need it to do it's job
	contents = []

	try:	
		for file in os.listdir('story'):
			with open(f'story/{file}') as c:
				lines = c.read().split('\n')
				start = 0
				end = 0
				i = 0
				for line in lines:
					if line.startswith('#'):
						label = line.strip().replace('#', '')
						if label.strip() == moment.strip():
							start = i
					i += 1
				i = 0
				for line in lines[start:]:
					if not line:
						end = start + i
						break
					i += 1
				contents = lines[start:end]
	except:
		success = False
		error = 'Failed to load story content'
		label = ''
		narrative = ''
		links = []
		return success, error, label, narrative, links

	try:
		label = contents[0].replace('#', '').strip()
		narrative = contents[1].strip()
		links = []
		for line in contents[3:]:
			data = line.split(' = ')
			hooks = data[0].split(', ')
			moments = data[1].split(', ')
			links.append([hooks, moments])
		success = True
		error = ''
		return success, error, label, narrative, links
	except:
		success = False
		error = 'The moment we found had nothing happening.'
		label = ''
		narrative = ''
		links = []
		return success, error, label, narrative, links


def main():
	# main gameplay loop
	# we need a 'pointer' to tell the game where we are in the
	# story file, and a rewind variable to keep track of the
	# previous pointer, because we may need to back-track;
	# pointer has a default value of somewhere in the story
	pointer = 'awake'
	rewind = pointer
	while True:
		print()
		# start looping
		# first ask for a breakdown of the current moment, which
		# you provide with the pointer (pointer = name of moment)
		success, error, moment, narrative, links = read(pointer)
		if success:
			# now we're in the game
			# mark this as the previous pointer in case the next
			# one isn't succesful
			rewind = pointer
			# display the current moment's narrative
			print(narrative)
			print()
			# ask the player for their action
			action = input('What do you do? >> ')
			if action:
				# allow the player to exit with the special
				# command: !quit
				if action == '!quit':
					break
				# if the story file is well written, we should
				# be able to find a new moment to get to from
				# the user's input; set the pointer there and
				# then go back to the start of the loop
				pointer = choose_from_links(action, links)
			else:
				# if user provided nothing and hit enter,
				# just re-deliver the narration and let
				# them try again
				print()
		else:
			# if we are here, we couldn't find a moment
			# to move to from the user's input, OR the
			# moment exists but there is incomplete data;
			# so we'll have to rewind to the previous moment
			# and run the loop again
			pointer = rewind


if __name__ == '__main__':
	# run the game
	main()