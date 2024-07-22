# tid a time orderable id.
## b32alphabet
```
0                             32
234567abcdefghijklmnopqrstuvwxyz
```
We sort the b32 alphabet to maintain the same sort order between the 
b32 string and int64 encodings of TIDs
'0' is omitted to avoid confusion with 'o'
'1' is omitted to avoid confusion with 'l'

## timestamp
Timestamp is microseconds since unix epoch (1970-01-01T00:00:00+00:00)
A ID generator should give out the current microsecond since epoch or (last + 1)
witch ever is grater. `max(now, last + 1)`

## ClockID
clockID is a 10 bit field
0-31, "20" - "2z" are reserved for best effort TIDs.
32-991, "30" - "yz" are for context dependent use.
992-1023, "z0" - "zz" are reserved for globally unique TIDs.

best effort ClockIDs can be generated without coordination but may collide.

context dependent should be use in the context of a specific application.
The application developer should take steps to ensure the that in any given
time range range a ClockID is not reused. No process is specified for handling
leasing of (ClockID, time range) pairs.

globally unique ClockIDs should only be used after being added to this document
as a operator of one of the global ClockID operators.

| ClockID | URL               | public key | from          | to      |
|---------|-------------------|------------|---------------|---------|
| z0      | http://ccn.bz/tid | todo       | 2222-222-2222 | ongoing |

## string format
the ID has two parts the timestamp and the ClockID.
the string format is 11 characters of time and 2 characters of clock.
This gives us 2**54 microseconds of time centered on the unix epoch and 1024 ClockIDs

TTTT-TTT-TTTT-CC

Since each char is 5 bits we need to sign extend the 54 bits to 55 bits
to convert to 11 char of b32.

```
3kxn-lhr-3gxq-23
 | |   |    |  |
 | |   |    |  ClockID 0-1023
 | |   |    microsecond
 | |   second
 | 10 hours (9.54 hours)
 year (1.115 years)
```

| start                       | end                          | tid            |
|-----------------------------|------------------------------|----------------|
|`2024-07-19T09:40:46.480310` | `2024-07-19T09:40:46.480310` | `3kxn-lhr-3gxq`|
|`2024-07-19T09:40:46.434304` | `2024-07-19T09:40:47.482879` | `3kxn-lhr`     |
|`2024-07-19T04:28:52.498432` | `2024-07-19T14:01:32.236799` | `3kxn`         |
|`2023-07-08T13:57:40.263936` | `2024-08-18T19:23:52.352767` | `3k`           |


next
```
s222-222-2222 1684-07-28T00:12:25.259008 min  i64
2222-222-2222 1970-01-01T00:00:00.000000 zero i64
bzzz-zzz-zzzz 2255-06-05T23:47:34.740992 max  i64
```

## int64 format
i = timestamp * 1024 + ClockID

Storing TIDs in int64 form will sort in the same order as the string form.
This format enable efficient storage and processing of TIDs in languages that support int64.