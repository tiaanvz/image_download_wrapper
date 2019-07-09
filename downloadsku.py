import os
import sys
import getopt

from google_images_download import google_images_download
from datetime import date

def printhelp():
    print("downloadsku.py -f <skufile> -s <size> -t <format>")
    print("  where <size> is one of large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP")
    print("    default: >1024*768")
    print("  and <format> is one of jpg, gif, png, bmp, svg, webp, ico, raw")
    print("    default: jpg")

def log_error(msg):
    today = date.today()
    logfilename = "download_sku_error_" + today.isoformat() + ".log"
    with open(logfilename, "a+") as f:
        f.write(msg + os.linesep)

def log(msg):
    today = date.today()
    logfilename = "download_sku_log_" + today.isoformat() + ".log"
    with open(logfilename, "a+") as f:
        f.write(msg + os.linesep)

def main(argv):
    skufile = "sku.txt"
    size = ">1024*768"
    fmt = "jpg"
    try:
        opts, args = getopt.getopt(argv,"hf:s:t:")
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt == '-f':
            skufile = arg
        elif opt == '-s':
            size = arg
        elif opt == '-t':
            fmt = arg

    response = google_images_download.googleimagesdownload()
    with open(skufile, "r") as f:
        for line in f:
            sku = line.strip()
            args = {
                "keywords": "\""+sku+"\"",
                "limit": 1,
                "print_urls": False,
                "no_directory": True,
                "prefix": "temp",
                "format": fmt,
                "size": size
            }
            paths, err = response.download(args)
            if err == 0:
                try:
                    fullpath = paths["\""+sku+"\""][0]
                    dirname  = os.path.dirname(fullpath)
                    basename = os.path.basename(fullpath)
                    name, ext = os.path.splitext(basename)
                    newfullpath = os.path.join(dirname, sku+ext)
                    if os.path.isfile(newfullpath):
                        # os.remove(fullpath)
                        print("File exists, skipping rename")
                    else:
                        os.rename(fullpath, os.path.join(dirname, sku+ext))
                except:
                    err_msg = "Exception with file operations: '" + str(paths) + "' with args  '" + str(args) + "'"
                    log_error(err_msg)
                    print(err_msg)
                    print("continue...")
            else:
                err_msg = "Error in 'googleimagesdownload' with args: '" + str(args) + "'"
                log_error(err_msg)
                print(err_msg)
                print("continue...")

if __name__ == "__main__":
   main(sys.argv[1:])


# size: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP
# format: jpg, gif, png, bmp, svg, webp, ico, raw
