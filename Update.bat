set /p Input=Commit: 
git add .
git commit -m "%Input%"
git push -u origin main