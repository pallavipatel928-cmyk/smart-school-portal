# Smart School Portal - GitHub Deployment Script
# Run this after installing Git

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Smart School Portal - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 1: Git Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$userName = Read-Host "Enter your name (for Git commits)"
$userEmail = Read-Host "Enter your email (for Git commits)"

git config --global user.name "$userName"
git config --global user.email "$userEmail"

Write-Host "✓ Git configured successfully!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 2: Initialize Repository" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

git init
Write-Host "✓ Git repository initialized" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 3: Add Files" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

git add .
Write-Host "✓ All files added to Git" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 4: Create Initial Commit" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

git commit -m "Initial commit - Smart School Portal"
Write-Host "✓ Initial commit created" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 5: Rename Branch to Main" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

git branch -M main
Write-Host "✓ Branch renamed to 'main'" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 6: Connect to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Before continuing, create a repository on GitHub!" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host "2. Name: smart-school-portal" -ForegroundColor White
Write-Host "3. DO NOT initialize with README" -ForegroundColor White
Write-Host "4. Click 'Create repository'" -ForegroundColor White
Write-Host ""

$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/smart-school-portal.git)"

if ($repoUrl) {
    git remote add origin $repoUrl
    Write-Host "✓ Remote repository connected" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Step 7: Push to GitHub" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "NOTE: You'll need to login to GitHub" -ForegroundColor Yellow
    Write-Host "Use Personal Access Token as password (not your GitHub password)" -ForegroundColor Yellow
    Write-Host "Create token at: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host ""
    
    $confirm = Read-Host "Ready to push to GitHub? (Y/N)"
    
    if ($confirm -eq "Y" -or $confirm -eq "y") {
        git push -u origin main
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  ✓ SUCCESS!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your project is now on GitHub!" -ForegroundColor Green
        Write-Host "View it at: $repoUrl" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Push cancelled. Run this command when ready:" -ForegroundColor Yellow
        Write-Host "git push -u origin main" -ForegroundColor White
    }
} else {
    Write-Host "✗ Repository URL not provided" -ForegroundColor Red
    Write-Host "Run this command manually after creating GitHub repo:" -ForegroundColor Yellow
    Write-Host "git remote add origin YOUR_REPO_URL" -ForegroundColor White
    Write-Host "git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. View your project on GitHub" -ForegroundColor White
Write-Host "2. Deploy to live server (see DEPLOYMENT_GUIDE.md)" -ForegroundColor White
Write-Host "3. Share your repository link" -ForegroundColor White
Write-Host ""
pause
