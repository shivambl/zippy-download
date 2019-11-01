# read all lines from input.txt
with open("input.txt", "r") as input_file:
    all_lines = input_file.readlines()

# filter valid urls and get their html pages
import urllib.request
import re

regex_get_mod = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\)'
regex_get_filename = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\) \+ \"\/(\S+)\"'
regex_v_in_url = r'/v/'
regex_filehtml_in_url = r'/file.html[\n]*'

download_links = []
for line in all_lines:
    line = line.strip()
    # check we get response from url in line
    try:
        resp = urllib.request.urlopen(line)
    except ValueError:
        continue

    resp = resp.read().decode("utf8")

    result_v = re.search(regex_v_in_url, line)
    result_filehtml = re.search(regex_filehtml_in_url, line)
    result_mod = re.search(regex_get_mod, resp)
    result_filename = re.search(regex_get_filename, resp)

    if result_v is None or result_filehtml is None or result_mod is None or result_filename is None:
        continue
    else:
        url = line
        url = re.sub(regex_v_in_url, "/d/", url)
        url = re.sub(regex_filehtml_in_url, "/", url)
        mod = (int(result_mod.group(1)) % int(result_mod.group(2))) + (int(result_mod.group(3)) % int(result_mod.group(4)))
        url = url + str(mod) + "/"
        url = url + result_filename.group(5)
        download_links.append(url)

# write all download links to output.txt
with open("output.txt", "w") as output_file:
    for link in download_links:
        output_file.write(link + '\n')