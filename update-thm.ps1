# Run from repo root: .\update-thm.ps1
# Fetches live TryHackMe stats and pushes updated thm.json to GitHub.

Set-Location $PSScriptRoot

Write-Host "`n[1/3] Fetching TryHackMe stats..." -ForegroundColor Cyan
python scripts/fetch_thm_stats.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Fetch failed. Check your internet connection and try again." -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/3] Committing thm.json..." -ForegroundColor Cyan
git add data/thm.json
$diff = git diff --cached --name-only
if ($diff) {
    git commit -m "chore: update THM stats manually"
    Write-Host "[3/3] Pushing to GitHub..." -ForegroundColor Cyan
    git push
    Write-Host "`n[OK] Done! Stats updated and live." -ForegroundColor Green
} else {
    Write-Host "[i] No changes in thm.json — stats unchanged." -ForegroundColor Yellow
}
