#!/usr/bin/env python3
import sys
import wave
import socket
import time
import struct

def send_rtp(target_ip, target_port, wav_file):
    # Open WAV file
    wf = wave.open(wav_file, 'rb')

    if wf.getframerate() != 8000 or wf.getnchannels() != 1:
        print("Please use an 8kHz mono WAV file (PCMU or raw).")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    seq = 0
    timestamp = 0
    ssrc = 12345  # random source id

    print(f"Streaming {wav_file} to {target_ip}:{target_port} ...")

    while True:
        data = wf.readframes(160)  # 20ms at 8000Hz
        if not data:
            break

        # RTP header (12 bytes)
        version = 2
        padding = 0
        extension = 0
        csrc_count = 0
        marker = 0
        payload_type = 0  # PCMU
        header = struct.pack("!BBHII",
                             (version << 6) | (padding << 5) | (extension << 4) | csrc_count,
                             (marker << 7) | payload_type,
                             seq, timestamp, ssrc)

        sock.sendto(header + data, (target_ip, int(target_port)))

        seq = (seq + 1) % 65536
        timestamp += 160  # 20ms for 8000Hz

        time.sleep(0.02)  # 20ms delay to maintain timing

    sock.close()
    wf.close()
    print("RTP stream finished.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 asterisk_rtp_send.py <target_ip> <target_port> <wav_file>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    wav_file = sys.argv[3]
    send_rtp(target_ip, target_port, wav_file)
#!/usr/bin/env python3
import sys
import wave
import socket
import time
import struct

def send_rtp(target_ip, target_port, wav_file):
    # Open WAV file
    wf = wave.open(wav_file, 'rb')

    if wf.getframerate() != 8000 or wf.getnchannels() != 1:
        print("Please use an 8kHz mono WAV file (PCMU or raw).")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    seq = 0
    timestamp = 0
    ssrc = 12345  # random source id

    print(f"Streaming {wav_file} to {target_ip}:{target_port} ...")

    while True:
        data = wf.readframes(160)  # 20ms at 8000Hz
        if not data:
            break

        # RTP header (12 bytes)
        version = 2
        padding = 0
        extension = 0
        csrc_count = 0
        marker = 0
        payload_type = 0  # PCMU
        header = struct.pack("!BBHII",
                             (version << 6) | (padding << 5) | (extension << 4) | csrc_count,
                             (marker << 7) | payload_type,
                             seq, timestamp, ssrc)

        sock.sendto(header + data, (target_ip, int(target_port)))

        seq = (seq + 1) % 65536
        timestamp += 160  # 20ms for 8000Hz

        time.sleep(0.02)  # 20ms delay to maintain timing

    sock.close()
    wf.close()
    print("RTP stream finished.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 asterisk_rtp_send.py <target_ip> <target_port> <wav_file>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    wav_file = sys.argv[3]
    send_rtp(target_ip, target_port, wav_file)
#!/usr/bin/env python3
import sys
import wave
import socket
import time
import struct

def send_rtp(target_ip, target_port, wav_file):
    # Open WAV file
    wf = wave.open(wav_file, 'rb')

    if wf.getframerate() != 8000 or wf.getnchannels() != 1:
        print("Please use an 8kHz mono WAV file (PCMU or raw).")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    seq = 0
    timestamp = 0
    ssrc = 12345  # random source id

    print(f"Streaming {wav_file} to {target_ip}:{target_port} ...")

    while True:
        data = wf.readframes(160)  # 20ms at 8000Hz
        if not data:
            break

        # RTP header (12 bytes)
        version = 2
        padding = 0
        extension = 0
        csrc_count = 0
        marker = 0
        payload_type = 0  # PCMU
        header = struct.pack("!BBHII",
                             (version << 6) | (padding << 5) | (extension << 4) | csrc_count,
                             (marker << 7) | payload_type,
                             seq, timestamp, ssrc)

        sock.sendto(header + data, (target_ip, int(target_port)))

        seq = (seq + 1) % 65536
        timestamp += 160  # 20ms for 8000Hz

        time.sleep(0.02)  # 20ms delay to maintain timing

    sock.close()
    wf.close()
    print("RTP stream finished.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 asterisk_rtp_send.py <target_ip> <target_port> <wav_file>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    wav_file = sys.argv[3]
    send_rtp(target_ip, target_port, wav_file)
