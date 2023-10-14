import os
from random import choice


def sanitize(text):
	# !
	# remove symbols / special chars
	# remove colloquialisms, bits, extras
	sanitized_text = text.lower().strip()
	return sanitized_text



def find_hook_from_action(action, links):

	# links:
	# [[[list of hooks], [list of moments]]]

	l = 0
	for link in links:
		
		# link:
		# [[list of hooks], [list of moments]]
		
		hooks = link[0]
		moments = link[1]

		# hooks:
		# [list of hooks]

		# moments:
		# [list of moments]

		for hook in hooks:
			if sanitize(action) == sanitize(hook):
				# print(links[l])

				choices = moments
				# print(choices)
				return choice(choices)

		l += 1



def get_moment(moment_label):
	# !
	# this function is massively ugly
	# so I'll clean it up later, for now
	# I just need it to do it's job
	contents = []
	for file in os.listdir('story'):
		with open(f'story/{file}') as c:
			lines = c.read().split('\n')
			start = 0
			end = 0
			i = 0
			for line in lines:
				if line.startswith('#'):
					label = line.strip().replace('#', '')
					if label.strip() == moment_label.strip():
						start = i
				i += 1
			i = 0
			for line in lines[start:]:
				if not line:
					end = start + i
					break
				i += 1
			contents = lines[start:end]
	label = contents[0].replace('#', '').strip()
	narrative = contents[1].strip()
	links = []
	for line in contents[3:]:
		data = line.split(' = ')
		hooks = data[0].split(', ')
		moments = data[1].split(', ')
		links.append([hooks, moments])
	return label, narrative, links


# label, narrative, links = get_moment('awake')
# print(label)
# print(narrative)
# print(links)

# x = find_hook_from_action('sleep', links)
# print(x)



def main():
	pointer = 'awake'
	while True:
		moment, narrative, links = get_moment(pointer)
		print(narrative)
		action = input("")
		pointer = find_hook_from_action(action, links)


main()