import argparse

parser = argparse.ArgumentParser(
    description="Get file download links from zippyshare webpage links",
    epilog="Script repository: https://github.com/ratherlongname/zippy-download"
)

parser.add_argument(
    '-i', '--input-file',
    default="input.txt",
    help="Use URLs from INPUT_FILE. Defaults to input.txt"
)

parser.add_argument(
    '-o', '--output-file',
    default="urls.txt",
    help="Store generated download URLs in OUTPUT_FILE. File is created if it doesn't exist, truncated if it does. Defaults to urls.txt"
)

args = parser.parse_args()
print(args.input_file, args.output_file)

# read all lines from INPUT_FILE
with open(args.input_file, "r") as input_file:
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

# write all download links to OUTPUT_FILE
with open(args.output_file, "w") as output_file:
    for link in download_links:
        output_file.write(link + '\n')