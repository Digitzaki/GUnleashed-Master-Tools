import os
import sys
import struct

def get_u32_be(buf, offset=0):
    return struct.unpack(">I", buf[offset:offset+4])[0]

def get_u16_be(buf, offset=0):
    return struct.unpack(">H", buf[offset:offset+2])[0]

def get_u8(buf, offset=0):
    return struct.unpack("B", buf[offset:offset+1])[0]

def put_u32_be(n):
    return struct.pack(">I", n)

def put_u16_be(n):
    return struct.pack(">H", n)

def nibbles_to_samples(nibbles):
    whole_frames = nibbles // 16
    remainder = nibbles % 16
    if remainder > 0:
        return (whole_frames * 14) + (remainder - 2)
    else:
        return whole_frames * 14

def main(argc=len(sys.argv), argv=sys.argv):
    if argc != 2:
        return

    sdir_path = os.path.realpath(argv[1])

    if not os.path.isfile(sdir_path):
        sys.exit("ERROR: Invalid path: %s" % sdir_path)

    samp_path = os.path.splitext(sdir_path)[0] + ".samp"

    if not os.path.isfile(samp_path):
        sys.exit("ERROR: Could not find sample file for %s" % os.path.basename(sdir_path))

    with open(sdir_path, "rb") as sdir:

        sdirhead = bytearray(16)

        sdir.readinto(sdirhead)

        if sdirhead[0:4][::-1] != b"SDIR": # not really sure if this is part of MusyX's data or the UBER VFS, but since Godzilla is the only Wii MusyX game I've seen ... *shrug*
            sys.exit("ERROR: Bad SDIR file")

        samp_size = get_u32_be(sdirhead, 0x08) # size of .samp file

        num_samples = get_u32_be(sdirhead, 0x0C) # number of entries/samples

        sampinfo = bytearray(64)

        with open(samp_path, "rb") as samp:

            for i in range(num_samples):

                sdir.readinto(sampinfo)

                sample_offset = get_u32_be(sampinfo, 0x00) # sample offset in nibbles
                num_nibbles   = get_u32_be(sampinfo, 0x04) # size of sound in nibbles
                loop_flag     =     get_u8(sampinfo, 0x0B)
                sample_rate   = get_u16_be(sampinfo, 0x0E)
                coefficients  = sampinfo[0x10:0x30] # decode coefficients
                ps            = sampinfo[0x33:0x34] # predictor/scale
                lps           = sampinfo[0x39:0x3A] # predictor/scale for loop context ??

                if num_nibbles > 0:

                    dsp_path = os.path.splitext(sdir_path)[0] + ("_%02d.dsp" % i)

                    with open(dsp_path, "wb") as dsp:

                            samp.seek((sample_offset - 2) // 2)
                            dspbuf = bytearray(96 + (num_nibbles // 2))
                            num_samples = nibbles_to_samples(num_nibbles)

                            dspbuf[0x00:0x04] = put_u32_be(num_samples) # 0x00 raw samples
                            dspbuf[0x04:0x08] = put_u32_be(num_nibbles) # 0x04 nibbles
                            dspbuf[0x08:0x0C] = put_u32_be(sample_rate) # 0x08 sample rate
                            dspbuf[0x0C:0x0E] = put_u16_be(0)           # 0x0C loop flag (not quite certain how loop info is stored yet, so 0)
                            dspbuf[0x0E:0x10] = put_u16_be(0)           # 0x0E format (always zero - ADPCM)
                            dspbuf[0x10:0x14] = put_u32_be(0)           # 0x10 loop start address (in nibbles)
                            dspbuf[0x14:0x18] = put_u32_be(0)           # 0x14 loop end address (in nibbles)
                            dspbuf[0x18:0x1C] = put_u32_be(2)           # 0x18 initial offset value (in nibbles)
                            dspbuf[0x1C:0x3C] = coefficients            # 0x1C coefficients
                            dspbuf[0x3C:0x3E] = put_u16_be(0)           # 0x3C gain (always zero for ADPCM)
                            dspbuf[0x3E:0x40] = b"\0" + ps              # 0x3E predictor/scale
                            dspbuf[0x40:0x42] = put_u16_be(0)           # 0x40 sample history (not specified?)
                            dspbuf[0x42:0x44] = put_u16_be(0)           # 0x42 sample history (not specified?)
                            dspbuf[0x44:0x46] = b"\0" + lps             # 0x44 predictor/scale for loop context
                            dspbuf[0x46:0x48] = put_u16_be(0)           # 0x46 sample history (n-1) for loop context
                            dspbuf[0x48:0x4A] = put_u16_be(0)           # 0x48 sample history (n-2) for loop context
                            dspbuf[0x4A:0x60] = b"\0" * 22              # 0x4A pad (reserved)

                            dspbuf[0x60:len(dspbuf)] = samp.read(num_nibbles // 2)

                            dsp.write(dspbuf)

    return 0

if __name__=="__main__":
    main()