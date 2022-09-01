Import-Csv .\Scheduled.csv | ForEach-Object {
    New-AzSentinelAlertRule -ResourceGroupName "AtopResource" -WorkspaceName "AtopResource" -Scheduled -Enabled -DisplayName $_.DisplayName -Severity $_.Severity -Query $_.Query -QueryFrequency (New-TimeSpan -Seconds  $_.QueryFrequency) -QueryPeriod (New-TimeSpan -Seconds $_.QueryPeriod) -TriggerThreshold $_.TriggerThreshold
    Start-Sleep -Seconds 1
}