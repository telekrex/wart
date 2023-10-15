#!/usr/bin/env python3
from random import choice
import os


def sanitize(text):
	# remove non alpha-numeric
	# characters from the text
	for character in text:
		if character.isalnum():
			pass
		else:
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
	pointer = 'awake'
	rewind = pointer
	while True:		
		success, error, moment, narrative, links = read(pointer)
		if success:
			rewind = pointer
			print(narrative)
			action = input('')
			if action:
				pointer = choose_from_links(action, links)
			else:
				# if user provided nothing and hit enter,
				# just re-deliver the narration and let
				# them try again.
				print('Empty!')
		else:
			# print(error)
			pointer = rewind


main()