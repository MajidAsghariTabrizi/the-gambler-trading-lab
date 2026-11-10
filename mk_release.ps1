Set-Location "D:\PycharmProjects\pythonProject\Trade\public_release\the-gambler-trading-lab"
$raw = Get-Content docs\launch\RELEASE_NOTES_v3.0.0.md -Raw
$json = @{ tag_name = 'v3.0.0'; name = 'The Gambler - Final Research Archive'; body = $raw } | ConvertTo-Json
[IO.File]::WriteAllText($env:TEMP + '\rel_payload.json', $json)
gh api repos/MajidAsghariTabrizi/the-gambler-trading-lab/releases --input ($env:TEMP + '\rel_payload.json') --jq .html_url
