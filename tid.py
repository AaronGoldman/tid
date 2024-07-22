from base64   import b32encode, b32decode
from datetime import datetime
from time     import time, sleep

# 2345-67a-bcde | 11 b32 | 55 bits | 1 sign 54 magnatude
# years [1,400 CE - 2,540 CE]
#   k222-222-2222 1399-02-23T00:24:50.518017 first
#   zzzz-zzz-zzzz 1969-12-31T23:59:59.999999 max
#   2222-222-2222 1970-01-01T00:00:00.000000 min
#   jzzz-zzz-zzzz 2540-11-07T23:35:09.481983 last
#
# 1,000,000 transactions per second max
# unix time in us b32 (microseconds since 1970)
#
# 2345          ~9.5 hours precision
# 2345-67a      ~1 second precision 
# 2345-67a-bcde microseconds precision

trans = b''.maketrans(
  b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
  b'234567abcdefghijklmnopqrstuvwxyz',
)

untrans = b''.maketrans(
  b'234567abcdefghijklmnopqrstuvwxyz',
  b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
)

def format_transaction(t):
  return f"{t[:4]}-{t[4:7]}-{t[7:11]}"

def transaction_from_timestamp(t_us):
  t_bytes = t_us.to_bytes(length=10, byteorder='big', signed=True)
  t_full = b32encode(t_bytes)
  t_translated = t_full.translate(trans).decode()
  t_formated = format_transaction(t_translated[5:])
  return t_formated

last_time = 0
def next():
  global last_time
  time_in_microseconds = int(time() * 1000000)
  last_time = max(last_time + 1, time_in_microseconds)
  return transaction_from_timestamp(last_time)

def iso_from_timestamp(t_timestamp):
  return datetime.fromtimestamp(t_timestamp).isoformat()

def transaction_to_timestamp(t):
  t_striped = t.replace('-','')
  prefix = b'22222' if t_striped < 'k' else b'zzzzz'
  suffix = b'22222222222' if t_striped < 'k' else b'zzzzzzzzzzz'
  t_extended = prefix + t_striped.encode() + suffix
  t_full = t_extended[:16]
  t_translated = t_full.translate(untrans)
  t_bytes = b32decode(t_translated)
  t_timestamp_us = int.from_bytes(bytes=t_bytes, byteorder='big', signed=True)
  t_timestamp = t_timestamp_us/1_000_000
  return t_timestamp

def transaction_to_iso(t):
  t_timestamp = transaction_to_timestamp(t)
  t_iso = iso_from_timestamp(t_timestamp)
  return t_iso

def transaction_to_iso_range(t):
  start = transaction_to_iso(t + '22222222222')
  end   = transaction_to_iso(t + 'zzzzzzzzzzz')
  return (start, end, t)

def main():
  print(transaction_to_iso_range("3kxn-lhr-3gxq"))
  print(transaction_to_iso_range("3kxn-lhr"     ))
  print(transaction_to_iso_range("3kxn"         ))
  print(transaction_to_iso_range("3k"           ))
  while True:
    sleep(.3)
    print(f'\r{next()}-22', end='')

if __name__ == "__main__":
  main()