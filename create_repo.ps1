$token = $env:GITHUB_TOKEN  # Use environment variable instead
$headers = @{
    "Authorization" = "token $token"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    name = "provon"
    description = "Provon - Document Q&A System with AI"
    private = $false
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method POST -Headers $headers -Body $body

Write-Host "Repository created successfully!"
Write-Host "Repository URL: $($response.html_url)"
