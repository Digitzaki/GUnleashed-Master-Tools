import os
import sys
import struct

def read_u32_be(f):
    return struct.unpack(">I", f.read(4))[0]

def bin2ascii(bin):
    try:
        str = bin.decode("ascii")
    except UnicodeError:
        return ""
    return str

def main(argc=len(sys.argv), argv=sys.argv):
    if argc < 2:
        print("Usage: %s <file.uber> ..." % argv[0])

    for arg in argv[1:]:
        uber_path = os.path.realpath(arg)
        uber_size = os.path.getsize(uber_path)

        if os.path.isfile(uber_path) is not True:
            print("ERROR: Invalid path: %s" % uber_path)
            continue

        with open(uber_path, "rb") as uber:
            uber.seek(0x08)
            offsets = []
            offset = read_u32_be(uber)
            offsets.append(offset)
            while uber.tell() < offsets[0]:
                offset = read_u32_be(uber)
                offsets.append(offset)
            offsets.append(uber_size)

            i = 0
            while uber.tell() < uber_size and i < len(offsets):
                size = offsets[i+1] - uber.tell()
                outbuf = uber.read(size)
                type = bin2ascii(outbuf[0:4])[::-1].lower()
                if type in ["sdir", "pool", "proj"]:
                    out_path = "%s.%s" % (os.path.splitext(uber_path)[0], type)
                else:
                    out_path = "%s_%02d.bin" % (os.path.splitext(uber_path)[0], i)
                with open(out_path, "wb") as out:
                    out.write(outbuf)
                i += 1

    return 0

if __name__=="__main__":
    main()