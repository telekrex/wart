#!/usr/bin/env python3
from random import choice
import os


def load_story(directory):
	story = []
	nons = []
	for file in os.listdir(directory):
		if file.startswith('.'):
			with open(f'{directory}/{file}') as f:
				nons = f.read().split('\n')
		else:
			with open(f'{directory}/{file}') as f:
				lines = f.read().split('\n')
				for line in lines:
					story.append(line)
	return story, nons


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


def choice_from_links(user_choice, links):
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
			if sanitize(user_choice)[0:4] == sanitize(hook)[0:4]:
				# we sanitize both user's input and the
				# story file contents just in case, and
				# to force them to be as close as possible
				return choice(moments)


def find_moment(story, moment):
	#
	moment = moment.strip().lower().replace('#', '')
	moment_start = 0
	moment_end = 0
	current_line_number = -1
	for line in story:
		current_line_number += 1
		if line.startswith('#'):
			label = line.strip().lower().replace('#', '')
			if label.strip() == moment.strip():
				moment_start = current_line_number
	counted_from_start = 0
	for line in story[moment_start:]:
		if not line:
			moment_end = moment_start + counted_from_start
			break
		counted_from_start += 1
	contents = story[moment_start:moment_end]
	label = contents[0].replace('#', '').strip()
	narrative = contents[1].strip()
	links = []
	for line in contents[3:]:
		data = line.split(' = ')
		hooks = data[0].split(', ')
		moments = data[1].split(', ')
		links.append([hooks, moments])
	return label, narrative, links




	# try:
	# 	label = contents[0].replace('#', '').strip()
	# 	narrative = contents[1].strip()
	# 	links = []
	# 	for line in contents[3:]:
	# 		data = line.split(' = ')
	# 		hooks = data[0].split(', ')
	# 		moments = data[1].split(', ')
	# 		links.append([hooks, moments])
	# 	success = True
	# 	error = ''
	# 	return success, error, label, narrative, links
	# except:
	# 	success = False
	# 	error = 'The moment we found had nothing happening.'
	# 	label = ''
	# 	narrative = ''
	# 	links = []
	# 	return success, error, label, narrative, links


def slate(text):
	#
	print('\n', text, '\n')
	action = input(' >> ')
	return action


def play(story_directory, starting_moment):
	# main gameplay loop
	# we need a 'pointer' to tell the game which
	# moment we are looking at, and right now,
	# it needs somewhere to start
	story, nons = load_story(story_directory)
	pointer = starting_moment

	x = 0
	while x < 99:
		x += 1
		try:
			moment, narration, links = find_moment(story, pointer)
		except:
			narration = choice(nons)
		action = slate(narration)
		pointer = choice_from_links(action, links)
		if action.lower() == 'quit':
			break


# 		print()
# 		# start looping
# 		# first ask for a breakdown of the current moment, which
# 		# you provide with the pointer (pointer = name of moment)
# 		success, error, moment, narrative, links = read(story_dir, pointer)
# 		if success:
# 			# now we're in the game
# 			# mark this as the previous pointer in case the next
# 			# one isn't succesful
# 			rewind = pointer
# 			# display the current moment's narrative
# 			print(narrative)
# 			print()
# 			# ask the player for their action
# 			action = input('What do you do? >> ')
# 			if action:
# 				# allow the player to exit with the special
# 				# command: !quit
# 				if action == 'QUIT':
# 					break
# 				# if the story file is well written, we should
# 				# be able to find a new moment to get to from
# 				# the user's input; set the pointer there and
# 				# then go back to the start of the loop
# 				pointer = choose_from_links(action, links)
# 			else:
# 				# if user provided nothing and hit enter,
# 				# just re-deliver the narration and let
# 				# them try again
# 				print()
# 		else:
# 			# if we are here, we couldn't find a moment
# 			# to move to from the user's input, OR the
# 			# moment exists but there is incomplete data;
# 			# so we'll have to rewind to the previous moment
# 			# and run the loop again
# 			pointer = rewind
# 			print(bat(story_dir))
