import json
import os
import requests
import sys

def examples():
    print(f"JS Source Map Extractor\n\nExample:\n\t{sys.argv[0]} ./source.map\n\t{sys.argv[0]} https://website.example.com/source.map")
    sys.exit(0)

def retrieveSourceMap(fileOrURL):
    sourceMap = None
    if os.path.isfile(sys.argv[1]):
        with open(fileOrURL, "r") as f:
            sourceMap = json.loads(f.read())
        print("Retrieved source map from file")
    elif fileOrURL.startswith("http"):
        sourceMap = json.loads(requests.get(sys.argv[1]).text)
        print("Retrieved source map from url")
    return sourceMap

def extractFiles(sourceMap):
    fileCount = len(sourceMap["sources"])
    for index, file in enumerate(sourceMap["sources"]):
        newFilePath = f".{os.sep}{file}"
        print(f"\r{str(index + 1)}/{str(fileCount)}\t{file.split('/')[:-1]}", end="")

        if not os.path.exists(newFilePath):
            if "/" in file: os.makedirs(os.sep.join(newFilePath.split('/')[:-1]), exist_ok=True)
            open(newFilePath, "wb").write(sourceMap["sourcesContent"][index].encode("utf8"))
        else:
            print(f"\rFile exists, skipping: {newFilePath}")

    print(f"\r{str(index + 1)}/{str(fileCount)}\tCompleted", end="")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        examples()

    sourceMap = retrieveSourceMap(sys.argv[1])
    if sourceMap != None:
        extractFiles(sourceMap)
