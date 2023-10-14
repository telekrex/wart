import os


class Moment:
	def __init__(self, contents):
	    self.contents = contents
	    self.label = contents[0].replace('#', '').strip()
	    self.narra = contents[1]
	    self.links = contents[3].split(' = ')
	    self.hooks = self.links[0].split(', ')
	    self.mmnts = self.links[1].split(', ')


def create_object_from_moment(moment):
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
			return Moment(lines[start:end])


mo = create_object_from_moment('nightmare')
print(mo.label)
print(mo.narra)
print(mo.hooks)
print(mo.mmnts)


# def main():
# 	while True:
# 		action = input("")