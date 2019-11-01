import argparse
import re
try:
    import urllib.request
    is_python_3 = True
except ImportError:
    import urllib2
    is_python_3 = False

regex_get_mod = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\)'
regex_get_filename = r'\((\d+) % (\d+) \+ (\d+) % (\d+)\) \+ \"\/(\S+)\"'
regex_v_in_url = r'/v/'
regex_filehtml_in_url = r'/file.html[\n]*'

# Create argument parser
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

# Read entire INPUT_FILE
try:
    with open(args.input_file, "r") as input_file:
        all_lines = input_file.readlines()
except IOError as e:
    print(e)
    exit()

# Get download link for each line from INPUT_FILE
download_links = []
for line in all_lines:
    # Trim whitespace
    line = line.strip()

    # Check line is URL giving valid response
    if is_python_3:
        try:
            resp = urllib.request.urlopen(line)
        except ValueError:
            continue
    else:
        try:
            resp = urllib2.urlopen(line)
        except ValueError:
            continue
    content = resp.read().decode("utf8")

    # Check URL syntax and response contents
    result_v = re.search(regex_v_in_url, line)
    result_filehtml = re.search(regex_filehtml_in_url, line)
    result_mod = re.search(regex_get_mod, content)
    result_filename = re.search(regex_get_filename, content)

    if result_v is None or result_filehtml is None or result_mod is None or result_filename is None:
        continue
    else:
        # Generate download link
        url = line
        url = re.sub(regex_v_in_url, "/d/", url)
        url = re.sub(regex_filehtml_in_url, "/", url)
        mod = (int(result_mod.group(1)) % int(result_mod.group(2))) + (int(result_mod.group(3)) % int(result_mod.group(4)))
        url = url + str(mod) + "/"
        url = url + result_filename.group(5)
        download_links.append(url)

# Write all download links to OUTPUT_FILE
if download_links:
    with open(args.output_file, "w") as output_file:
        for link in download_links:
            output_file.write(link + '\n')
    print("{} links written to file {}".format(len(download_links), args.output_file))
else:
    print("0 links generated.")