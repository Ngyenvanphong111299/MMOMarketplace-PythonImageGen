# Test API script cho Docker
$uri = "http://localhost:8001/generate-image"
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "XzEcSl7aaW7wfeyxW74IGpGDBcM4noaO"
}
$body = '{"category_name": "Công nghệ", "category_bg_color": "#0056FF", "category_text_color": "#FFFFFF", "content": "<div><h1>Test Article với Logo</h1><p>Nội dung test</p></div>", "background_theme": "technology, innovation", "logo_url": "https://example.com/logo.png", "show_logo": true}'
$bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)

Write-Host "Testing Docker API at $uri..."
try {
    $response = Invoke-WebRequest -Uri $uri -Method POST -Headers $headers -Body $bodyBytes -ContentType "application/json" -OutFile "test-image-docker.png"
    Write-Host "Success! Image saved to test-image-docker.png"
    Write-Host "Status Code: $($response.StatusCode)"
} catch {
    Write-Host "Error: $_"
    Write-Host "Response: $($_.Exception.Response)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody"
    }
}

