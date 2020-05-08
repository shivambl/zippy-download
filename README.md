# zippy-download

Input any number of zippy share links and run zippy-download.py. Direct download links to the files will be created. No need to manually open and click "Download Now" in zippy links.

## How to run

#### 1. Download this repository
```
$ git clone https://github.com/ratherlongname/zippy-download.git
```

#### 2. Put zippy links into input.txt

Put one link per line. If you have a .dlc container, use [dcrypt.it](www.dcrypt.it) to get all the links inside it.

#### 3. Run zippy-download.py
```
$ python3 zippy-download.py
```
Give it some time. It might seem like it's not working, but it is.

#### 4. Download files

All direct download links are generated in urls.txt. There are many ways to download these files:
  - Click on each link to download using your browser or default download manager
  - Download using [Xtreme Download Manager](https://subhra74.github.io/xdm/) which is pretty amazing at accelerating downloads
  - Use wget to download all files sequentially
	  ```
	  $ wget -i urls.txt
	  ```
  - Use wget and parallel to download all files in parallel
	  ```
	  $ sudo apt install parallel -y
	  $ cat urls.txt | parallel --gnu "wget {}"
	  ```