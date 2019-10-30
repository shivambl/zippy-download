# read all lines from input.txt
with open("input.txt", "r") as input_file:
    all_lines = input_file.readlines()

# filter valid urls and get their html pages
import urllib.request

all_responses = []
valid_urls = []
for line in all_lines:
    try:
        resp = urllib.request.urlopen(line)
    except ValueError:
        continue

    all_responses.append(resp.read().decode("utf8"))
    valid_urls.append(line)


# create file download links
import re

def alter_urls(s):
    ans = re.sub(r'/v/', "/d/", s)
    ans = re.sub(r'/file.html[\n]*', "/", ans)
    return ans

## remove file.html and replace v with d in original urls
download_links = list(map(alter_urls, valid_urls))

## get mod challenge from html and append to url
regex_get_mod = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\)'
all_mods = []
for resp in all_responses:
    result = re.search(regex_get_mod, resp)
    mod = (int(result.group(1)) % int(result.group(2))) + (int(result.group(3)) % int(result.group(4)))
    all_mods.append(mod)

for i, mod in enumerate(all_mods):
    download_links[i] = download_links[i] + str(mod) + '/'

# get filename from html and append to url
regex_get_filename = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\) \+ \"\/(\S+)\"'
all_names = []
for resp in all_responses:
    result = re.search(regex_get_filename, resp)
    all_names.append(result.group(5))

for i, name in enumerate(all_names):
    download_links[i] = download_links[i] + name

# write all download links to output.txt
with open("output.txt", "w") as output_file:
    for link in download_links:
        output_file.write(link + '\n')