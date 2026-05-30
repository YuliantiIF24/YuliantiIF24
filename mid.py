import argparse
import hashlib
import os

# ANSI Color Codes
CYAN    = '\033[96m'
GREEN   = '\033[92m'
YELLOW  = '\033[93m'
WHITE   = '\033[97m'
RESET   = '\033[0m'
BOLD    = '\033[1m'

def hitung_hash(filepath):
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()

def format_ukuran(bytes_val):
    if bytes_val < 1024:
        return f'{bytes_val} B'
    elif bytes_val < 1024**2:
        return f'{bytes_val/1024:.1f} KB'
    else:
        return f'{bytes_val/1024**2:.1f} MB'

def tampilkan_hash(filepath):
    if not os.path.exists(filepath):
        print(f'  Error: File "{filepath}" tidak ditemukan.')
        return
    md5_hash, sha256_hash = hitung_hash(filepath)
    ukuran = format_ukuran(os.path.getsize(filepath))
    sha_line1 = sha256_hash[:32]
    sha_line2 = sha256_hash[32:]
    lebar = 60
    print()
    print(f'{CYAN}\u2554' + '\u2550' * (lebar-2) + f'\u2557{RESET}')
    print(f'{CYAN}\u2551{RESET}' + f'{BOLD}{WHITE}' + ' HASH FILE '.center(lebar-2) + f'{RESET}{CYAN}\u2551{RESET}')
    print(f'{CYAN}\u255a' + '\u2550' * (lebar-2) + f'\u255d{RESET}')
    print(f'  {WHITE}File          :{RESET} {YELLOW}{filepath}{RESET}')
    print(f'  {WHITE}Ukuran        :{RESET} {YELLOW}{ukuran}{RESET}')
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)
    print(f'  {WHITE}MD5           :{RESET} {GREEN}{md5_hash}{RESET}')
    print(f'  {WHITE}Jumlah Karakter MD5    :{RESET} {YELLOW}{len(md5_hash)} karakter hex{RESET}')
    print(f'  {WHITE}SHA-256       :{RESET} {GREEN}{sha_line1}{RESET}')
    print(f'                    {GREEN}{sha_line2}{RESET}')
    print(f'  {WHITE}Jumlah Karakter SHA-256:{RESET} {YELLOW}{len(sha256_hash)} karakter hex{RESET}')
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)

def bandingkan_file(file1, file2):
    for f in [file1, file2]:
        if not os.path.exists(f):
            print(f'  Error: File "{f}" tidak ditemukan.')
            return
    md5_1, sha256_1 = hitung_hash(file1)
    md5_2, sha256_2 = hitung_hash(file2)
    uk1 = format_ukuran(os.path.getsize(file1))
    uk2 = format_ukuran(os.path.getsize(file2))
    lebar = 60
    print()
    print(f'{CYAN}\u2554' + '\u2550' * (lebar-2) + f'\u2557{RESET}')
    print(f'{CYAN}\u2551{RESET}' + f'{BOLD}{WHITE}' + ' PERBANDINGAN FILE '.center(lebar-2) + f'{RESET}{CYAN}\u2551{RESET}')
    print(f'{CYAN}\u255a' + '\u2550' * (lebar-2) + f'\u255d{RESET}')
    print(f'  {WHITE}FILE ASLI       :{RESET} {YELLOW}{file1}  ({uk1}){RESET}')
    print(f'  {WHITE}FILE MODIF      :{RESET} {YELLOW}{file2}  ({uk2}){RESET}')
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)
    print()
    print(f'  {BOLD}{WHITE}[ MD5 ]{RESET}')
    print(f'  {WHITE}Asli     :{RESET} {GREEN}{md5_1}{RESET}')
    print(f'  {WHITE}Modif    :{RESET} {GREEN}{md5_2}{RESET}')
    print(f'  {WHITE}Jumlah Karakter MD5    :{RESET} {YELLOW}{len(md5_1)} karakter hex{RESET}')
    print()
    print(f'  {BOLD}{WHITE}[ SHA-256 ]{RESET}')
    print(f'  {WHITE}Asli     :{RESET} {GREEN}{sha256_1[:32]}{RESET}')
    print(f'             {GREEN}{sha256_1[32:]}{RESET}')
    print(f'  {WHITE}Modif    :{RESET} {GREEN}{sha256_2[:32]}{RESET}')
    print(f'             {GREEN}{sha256_2[32:]}{RESET}')
    print(f'  {WHITE}Jumlah Karakter SHA-256:{RESET} {YELLOW}{len(sha256_1)} karakter hex{RESET}')
    print()
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)
    print(f'  {BOLD}{WHITE}HASIL PERBANDINGAN{RESET}')
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)
    md5_sama  = md5_1 == md5_2
    sha_sama  = sha256_1 == sha256_2
    md5_status  = f'\033[92m\u2714  SAMA{RESET}' if md5_sama  else f'\033[91m\u2718  BERBEDA \u2014 file telah dimodifikasi{RESET}'
    sha_status  = f'\033[92m\u2714  SAMA{RESET}' if sha_sama  else f'\033[91m\u2718  BERBEDA \u2014 file telah dimodifikasi{RESET}'
    print(f'  {WHITE}MD5        :{RESET} {md5_status}')
    print(f'  {WHITE}SHA-256    :{RESET} {sha_status}')
    print(f'{CYAN}  ' + '\u2500' * (lebar-2) + RESET)

def main():
    parser = argparse.ArgumentParser(
        description='Aplikasi pengecekan integritas file menggunakan MD5 dan SHA-256.'
    )
    subparsers = parser.add_subparsers(dest='command')

    hash_parser = subparsers.add_parser('hash',
        help='Tampilkan hash MD5 dan SHA-256 untuk sebuah file.')
    hash_parser.add_argument('file', type=str)

    cmp_parser = subparsers.add_parser('compare',
        help='Bandingkan dua file berdasarkan hash mereka.')
    cmp_parser.add_argument('file1', type=str)
    cmp_parser.add_argument('file2', type=str)

    args = parser.parse_args()
    if args.command == 'hash':
        tampilkan_hash(args.file)
    elif args.command == 'compare':
        bandingkan_file(args.file1, args.file2)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()