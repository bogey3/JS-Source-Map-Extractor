#!/usr/bin/python3
import json
import os
import requests
import sys

def examples():
    print(f"JS Source Map Extractor\n\nExample:\n\t{sys.argv[0]} ./source.map\n\t{sys.argv[0]} https://website.example.com/source.map")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        examples()

    sourceMap = None
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "r") as f:
            sourceMap = json.loads(f.read())
        print("Retrieved source map from file")
    elif sys.argv[1].startswith("http"):
        sourceMap = json.loads(requests.get(sys.argv[1]).text)
        print("Retrieved source map from url")
    else:
        examples()

    fileCount = len(sourceMap["sources"])
    for index, file in enumerate(sourceMap["sources"]):
        print(f"\r{str(index+1)}/{str(fileCount)}\t{file.split('/')[:-1]}", end="")
        if not os.path.exists(f".{os.sep}{file}"):
            if "/" in file: os.makedirs(f".{os.sep}{os.sep.join(file.split('/')[:-1])}", exist_ok=True)
            open(f".{os.sep}{file}", "wb").write(sourceMap["sourcesContent"][index].encode("utf8"))
        else:
            print(f"\rFile exists, skipping: {file}")

    print(f"\r{str(index + 1)}/{str(fileCount)}\tCompleted", end="")
