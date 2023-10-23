#!/usr/bin/env python3
from random import choice
import os


def load_story(directory):
	# force directory into string type
	directory = str(directory)
	story = []
	nons = []
	# loop over files in the directory
	for file in os.listdir(directory):
		if file.startswith('.'):
			# files starting with . are used to list
			# responses to game not finding something
			# to do with the user's input. I want to
			# change this at some point to be stored
			# within any story file along with the
			# moments. sometime later.
			with open(f'{directory}/{file}') as f:
				nons = f.read().split('\n')
		else:
			# otherwise, the file can be used for
			# story content. grab the lines.
			with open(f'{directory}/{file}') as f:
				lines = f.read().split('\n')
				for line in lines:
					story.append(line)
	# return both the 'nons' and the story content
	# as two lists, one for each.
	return story, nons


def simplify(text):
	# this function AGGRESSIVELY
	# cuts down the input text to
	# a form that's not only super
	# simple, but easy to match with
	# hooks placed in author's stories.
	# first,
	# remove terms from the text
	# that will never be useful
	text = str(text)
	for term in [' the ', ' a ', 'use ', ' use ',
				 'put ', 'do ', ' do ', 'go ', ' go ',
				 'stay ', 'put ']:
		text = text.replace(term, '')
	# then, split the text
	# into a list of its terms
	terms = text.split(' ')
	# rebuild the text, but
	# without the spaces
	text = ''.join(text)
	return text


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
	# first, quickly, verify the contents of
	# user choice as a string and simplify
	user_choice = simplify(str(user_choice))
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
			# simplify the hook
			hook = simplify(hook)
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
	# force moment to be cleaner
	moment = moment.strip().lower()
	moment_start = 0
	moment_end = 0
	current_line_number = -1
	# look over every line in the story content
	for line in story:
		current_line_number += 1
		if line.startswith('#'):
			# lines starting with # mark a moment; but we
			# need to find the correct one...
			# force the line to be cleaner so we can look
			label = line.strip().lower().replace('#', '')
			if label.strip() == moment.strip():
				# if we found a match, that's our guy;
				# mark the line number this is at
				moment_start = current_line_number
	# now we're going to start counting from there
	counted_from_start = 0
	# look over each line, starting from there
	for line in story[moment_start:]:
		if not line:
			# if a line was empty, this is where the author
			# is separating the moment from another with a
			# blank line; it's where we want to stop looking
			moment_end = moment_start + counted_from_start
			break
		# if we hadn't hit a blank line yet,
		# increase the count and keep looking
		counted_from_start += 1
	# now we grab a slice from the line that
	# starts the moment, to the line that ends it
	contents = story[moment_start:moment_end]
	# then we need to sort out:
	# label is the name of the moment, in case needed
	label = contents[0].replace('#', '').strip()
	# narrative is the narration of the moment
	# this can be multiple lines, so we'll build
	# a list going from index 1 until we hit the
	# '-' delimiter
	narrative = []
	narr_end = 1
	for line in contents[1:]:
		if line != '-':
			narrative.append(line)
			narr_end += 1
		else:
			break
	# links are a list of two lists;
	# one is the hooks that match user input,
	# the other is the corresponding potential
	# moments to call from a hook
	links = []
	for line in contents[narr_end+1:]:
		data = line.split(' = ')
		hooks = data[0].split(', ')
		moments = data[1].split(', ')
		links.append([hooks, moments])
	# now that we've got a moment and its pieces,
	# return that to the game
	return label, narrative, links


def slate(text):
	# show the given text
	print()
	for line in text:
		print(line)
	print()
	# then ask for a reponse
	action = input('> ')
	return action


def play(story_directory, starting_moment):
	# main gameplay loop
	# load the story and put its contents into
	# two lists, story and nons from the function
	story, nons = load_story(story_directory)
	# we need a pointer, this is going to tell
	# the game what moment we are looking at
	# when we go through the loop; start with
	# the given starting moment
	pointer = starting_moment
	# eventually this should be a better solution,
	# but for now I combine counting with a try/except
	# (yes, do try not to cringe, veteran programmers)
	# to ensure that an infinite loop can't hang the game.
	# anyways, we start looping...
	x = 0
	while x < 99:
		x += 1
		try:
			# try to find a moment within the story content from
			# the pointer, which should equal the name of a moment,
			# and in return we should have a new narration, and a
			# set of links to look through.
			moment, narration, links = find_moment(story, pointer)
		except:
			# if a moment could not be found, it's because either
			# the user put in something that doesn't yield a result,
			# or there was an error in the search. if this happens,
			# do not fret; we will give the user a response from
			# nons, that is why that exists, and why it's designed
			# to be customizable. you can use this to tell the player
			# things like how silly they are being.
			narration = [choice(nons)]
		# in either case, once we are at this poing in the loop,
		# we should have a narration to provide one way or another.
		# show that to the player, and ask for input.
		action = slate(narration)
		# then the pointer gets moved to a new position;
		# if choice from links cannot be found, we should
		# end up back at the slate with a nons narration
		pointer = choice_from_links(action, links)
		# give the user an exit if they desire
		if action.lower() == 'quit':
			break
