import json
import os
import requests
import sys
import re

def examples():
    print(f"JS Source Map Extractor\n\nExample:\n\t{sys.argv[0]} ./source.map\n\t{sys.argv[0]} https://website.example.com/source.map")
    sys.exit(0)

def retrieveSourceMap(fileOrURL):
    sourceMap = None
    size = 0
    if os.path.isfile(sys.argv[1]):
        with open(fileOrURL, "rb") as f:
            data = f.read().decode("utf8")
            size = len(data)
            sourceMap = json.loads(data)
        print("Retrieved source map from file")
    elif fileOrURL.startswith("http"):
        data = requests.get(sys.argv[1]).text
        size = len(data)
        print("Retrieved source map from url")
        sourceMap = json.loads(data)
    print(f"Parsed JSON ({str(size)} bytes)")
    return sourceMap

def extractFiles(sourceMap):
    characterReplaceRegex = re.compile(r"[<>:\"\/\|?*]")
    fileCount = len(sourceMap["sources"])
    maxStatus = 0
    for index, file in enumerate(sourceMap["sources"]):
        newFilePath = f".{os.sep}{os.sep.join(file.split('/'))}"
        newFilePath = characterReplaceRegex.sub("", newFilePath)
        status = f"\r{str(index + 1)}/{str(fileCount)}\t{newFilePath}"
        if len(status)>maxStatus:
            maxStatus = len(status)
        print(status + " "*(maxStatus - len(status)), end="")

        if not os.path.exists(newFilePath):
            if "/" in file:
                os.makedirs(os.sep.join(newFilePath.split(os.sep)[:-1]), exist_ok=True)
            open(newFilePath, "wb").write(sourceMap["sourcesContent"][index].encode("utf8"))
        else:
            print(f"\rFile exists, skipping: {newFilePath}")

    print(f"\r{str(index + 1)}/{str(fileCount)}\tCompleted", end="")

def buildFolderStructure(sourceMap):
    top = 0
    for file in sourceMap["sources"]:
        up = file.count(f"../")
        if up > top:
            top = up

    currentDir = sourceMap["file"].split("/")[:-1]
    for i in range(len(currentDir), top):
        currentDir = ["Unknown Folder"] + currentDir
    currentDir = [sourceMap["file"].split("/")[-1]] + currentDir
    dirString = f".{os.sep}{os.sep.join(currentDir)}"
    os.makedirs(dirString, exist_ok=True)
    os.chdir(dirString)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        examples()

    sourceMap = retrieveSourceMap(sys.argv[1])
    if sourceMap != None:
        buildFolderStructure(sourceMap)
        extractFiles(sourceMap)
