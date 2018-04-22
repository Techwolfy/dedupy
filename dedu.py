#!/usr/bin/python3
import argparse
import hashlib
import sys
import os

def hashdir(path, recurse):
	hashes = {}
	if recurse:
		files = []
		for root, dirs, filenames in os.walk(path):
			for f in filenames:
				files.append(os.path.join(root, f))
	else:
		files = os.listdir(path)
	total = len(files)
	cur = 0
	print('{} [0/{}]'.format(path, total), end='\r', flush=True)

	for filename in files:
		if recurse:
			fpath = filename
		else:
			fpath = os.path.join(path, filename)
		if not os.path.isfile(fpath):
			continue
		h = hashlib.sha256(open(fpath, 'rb').read()).hexdigest()
		hashes[h] = fpath

		cur += 1
		print('{} [{}/{}]'.format(path, cur, total), end='\r', flush=True)

	print('{} [{}/{}]'.format(path, cur, total))
	return hashes

def main(source, target, recurse, delete, force):
	print('Computing hashes...')
	s = hashdir(source, recurse)
	t = hashdir(target, recurse)

	both = {}
	src = dict(s)
	tgt = dict(t)

	print('\nComparing files...')
	for fhash, fname in s.items():
		if fhash in t:
			both[fhash] = [fname, t[fhash]]
			del src[fhash]
			del tgt[fhash]

	print('\nDuplicate files ({}):'.format(len(both)))
	for fhash, fnames in both.items():
		print('{}\t{}\t{}'.format(fhash, fnames[0], fnames[1]))

	print('\nUnique files in `{}` ({}):'.format(source, len(src)))
	for fhash, fname in src.items():
		print('{}\t{}'.format(fhash, fname))

	print('\nUnique files in `{}` ({}):'.format(target, len(tgt)))
	for fhash, fname in tgt.items():
		print('{}\t{}'.format(fhash, fname))

	if delete and (force or input('\nDelete duplicate files from {}? (y/N) '.format(target)).lower().startswith('y')):
		print('Deleting duplicate files...')
		for fhash, fnames in both.items():
			os.remove(fnames[1])
		print('Duplicate files removed.')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Deduplicate files by hash.')
	parser.add_argument('source', help='read-only source directory to compare files against')
	parser.add_argument('target', help='target directory to compare and remove files')
	parser.add_argument('-r', '--recurse', help='compare files in subdirectories', action='store_true', default=False)
	parser.add_argument('-d', '--delete', help='delete duplicate files in target directory', action='store_true', default=False)
	parser.add_argument('-f', '--force', help='delete files without asking for confirmation', action='store_true', default=False)
	args = parser.parse_args()
	main(args.source, args.target, args.recurse, args.delete, args.force)
