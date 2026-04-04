# Birthday VM Shutdown Write-up

## Challenge summary

Find the time when the system last shutdown started and submit it as:
`HRCTF{EPOCH_TIMESTAMP}`

## Reliable source used

Windows System event log inside the VM.

## Event to use

- Event ID `1074` (Provider `User32`)
- This event records a shutdown initiation request (shutdown start signal).

## PowerShell command inside VM

```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents 1 |
Format-Table TimeCreated, Id, ProviderName, Message -Wrap
```

## Convert timestamp to epoch

Use VM local timestamp and convert with timezone awareness:

```powershell
$e = Get-WinEvent -FilterHashtable @{LogName='System'; Id=1074} -MaxEvents 1
([DateTimeOffset]$e.TimeCreated).ToUnixTimeSeconds()
```

## Candidate from current solve session

- Observed TimeCreated: `12-12-2025 19:14:34`
- If interpreted in `Asia/Kolkata`, epoch seconds: `1765547074`
- Candidate flag: `HRCTF{1765547074}`

## Note

If checker rejects, verify whether challenge expects:

- UTC-interpreted conversion of displayed time, or
- a different shutdown marker (for example kernel/system service event), or
- epoch in milliseconds.
