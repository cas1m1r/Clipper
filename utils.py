import os


def cmd(cstr):
	result = b''
	err = 0
	proc = os.popen(cstr)
	try:
		result = proc.read()
	except OS.Error:
		err = 1
		pass
	proc.close()	
	return result, err


def get_formats(url):
	test = cmd(f'yt-dlp -F {sample_url}')
	clip_types = []
	for ln in test[0].split('\n'):
		fields = remove_empty(ln.split(' '))
		if len(fields) > 2:
			media_type = fields[1]
			if media_type == 'mp4':
				clip_types.append(f'{fields[0]} {fields[2]}')
	return clip_types

def remove_empty(elements):
	out = []
	for e in elements:
		if e not in out and len(e):
			out.append(e)
	return out
