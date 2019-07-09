import os
import sys
import getopt

from google_images_download import google_images_download

def printhelp():
    print("downloadsku.py -f <skufile> -s <size> -t <format>")
    print("  where <size> is one of large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP")
    print("    default: >1024*768")
    print("  and <format> is one of jpg, gif, png, bmp, svg, webp, ico, raw")
    print("    default: jpg")

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
                "prefix": sku,
                "format": fmt,
                "size": size
            }
            paths, err = response.download(args)
            fullpath = paths["\""+sku+"\""][0]
            dirname  = os.path.dirname(fullpath)
            basename = os.path.basename(fullpath)
            name, ext = os.path.splitext(basename)
            os.rename(fullpath, os.path.join(dirname, sku+ext))

if __name__ == "__main__":
   main(sys.argv[1:])


# size: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP
# format: jpg, gif, png, bmp, svg, webp, ico, raw
