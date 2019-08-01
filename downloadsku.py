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

def get_options(argv):
    # defaults
    options = {
        'skufile': "sku.txt",
        'size'   : ">1024*768",
        'fmt'    : "jpg"
    }
    # get opts
    try:
        opts, args = getopt.getopt(argv, "hf:s:t:")
    except getopt.GetoptError:
        printhelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt == '-f':
            options['skufile'] = arg
        elif opt == '-s':
            options['size'] = arg
        elif opt == '-t':
            options['fmt'] = arg
    return options

def enquote(val):
    return "\"" + val + "\""

def do_file_operations(paths, sku, args):
    k1 = list(paths)[0]
    if len(paths[k1]) > 0:
        try:
            fullpath    = paths[k1][0]
            dirname     = os.path.dirname(fullpath)
            basename    = os.path.basename(fullpath)
            name, ext   = os.path.splitext(basename)
            newfullpath = os.path.join(dirname, sku+ext)
            if os.path.isfile(newfullpath):
                print("File exists, skipping rename")
            else:
                os.rename(fullpath, os.path.join(dirname, sku+ext))
        except:
            err_msg = "Exception with file operations: '" + str(paths) + "' with args  '" + str(args) + "'"
            log_error(err_msg)
            print(err_msg)
            print("continue...")
    else:
        err_msg = "*** image not found for '" + sku + "' ***"
        log_error(err_msg)
        print(err_msg)

def main(argv):
    opts = get_options(argv)
    response = google_images_download.googleimagesdownload()
    print(opts)
    with open(opts['skufile'], "r") as f:
        for line in f:
            terms = line.strip().split(',')
            args = {
                'keywords'        : enquote(terms[0]),
                'suffix_keywords' : terms[1] if len(terms) > 1 else "",
                'limit'           : 1,
                'print_urls'      : False,
                'no_directory'    : True,
                'prefix'          : "temp",
                'format'          : opts['fmt'],
                'size'            : opts['size']
            }
            paths, err = response.download(args)
            do_file_operations(paths, terms[0], args)

if __name__ == "__main__":
   main(sys.argv[1:])

# size: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP
# format: jpg, gif, png, bmp, svg, webp, ico, raw
