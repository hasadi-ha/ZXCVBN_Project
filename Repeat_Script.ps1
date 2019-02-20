1..1 | % {
   $MaxThreads = 1
   While (@(Get-Job | Where { $_.State -eq "Running" }).Count -ge $MaxThreads)
   {  Write-Host "Waiting for open thread...($MaxThreads Maximum)"
      Start-Sleep -Seconds 3
   }
 
   $Scriptblock = {
      Param (
         [string]$CN
      )
      python C:\Users\BigH\Downloads\ZXCVBN_Project-master\tester2.py
   }
   Start-Job -ScriptBlock $Scriptblock -ArgumentList "."
}
 
While (@(Get-Job | Where { $_.State -eq "Running" }).Count -ne 0)
{  Write-Host "Waiting for background jobs..."
   Get-Job    #Just showing all the jobs
   Start-Sleep -Seconds 3
}
 
Get-Job       #Just showing all the jobs
$Data = ForEach ($Job in (Get-Job)) {
   Receive-Job $Job
   Remove-Job $Job
}
 
$Data | Select ProcessName,Product,ProductVersion | Format-Table -AutoSize