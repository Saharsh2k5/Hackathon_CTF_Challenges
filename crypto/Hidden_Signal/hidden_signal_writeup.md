# Hidden Signal Write-up

## Challenge summary

A hidden 8-digit integer was embedded in text spacing.

## Observation

The sentence contains irregular spacing between words.

## Decoding rule

- Single space = `0`
- Double space = `1`

## Steps

1. Extract each run of spaces between words.
2. Convert each run to a bit using the rule above.
3. Join bits into one binary string.
4. Convert binary to decimal.

## Result

- Binary: `000010011000001111100010111110`
- Decimal code: `39909566`
- Flag: `HRCTF{39909566}`
