## VEEAM Backups for Microsoft Office 365
## This powershell script needs to be run with the 64bit powershell
## and thus from a 64bit check_mk agent
## If a 64 bit check_mk agent is available it just needs to be renamed with
## the extension .ps1
## If only a 32bit  check_mk agent is available it needs to be relocated to a
## directory given in veeam_backup_status.bat and the .bat file needs to be
## started by the check_mk agent instead.


$pshost = get-host
$pswindow = $pshost.ui.rawui

$newsize = $pswindow.buffersize
$newsize.height = 300
$newsize.width = 150
$pswindow.buffersize = $newsize

Get-PSSnapin -Registered

try
{
$o365Jobs = Get-VBOJob
write-host "<<<veeam_o365jobs:sep(9)>>>"
foreach ($o365Job in $o365Jobs)
    {
        $jobID = $o365Job.Id
        $jobOrganisation = $o365Job.Organization.Name
        $jobName = $o365Job.Name
                
        $o365JobLastState = $o365Job.LastStatus

        $o365JobLastSession = Get-VBOJobSession -Job $o365Job -Last

        if ($o365JobLastSession -ne $null) {

            $o365JobCreationTime = $o365JobLastSession.CreationTime |  get-date -Format "dd.MM.yyyy HH\:mm\:ss" -ErrorAction SilentlyContinue

            $o365JobEndTime = $o365JobLastSession.EndTime |  get-date -Format "dd.MM.yyyy HH\:mm\:ss" -ErrorAction SilentlyContinue

            $o365JobDuration = $($o365JobLastSession.EndTime - $o365JobLastSession.CreationTime).TotalSeconds -as [int]

            $processed = $o365JobLastSession.Statistics.ProcessedObjects -as [int]

            if ($o365JobLastSession.Statistics.TransferredData -match '\d+(\.\d+)? [A-Z]B') {
                $transferred = $(Invoke-Expression -Command ($o365JobLastSession.Statistics.TransferredData -replace ' ')) -as [long]
            }

        } else {

            $o365JobCreationTime = "01.01.1970 00:00:00"
            $o365JobEndTime = "01.01.1970 00:00:00"
            $o365JobDuration = 0
            $processed = 0
            $transferred = 0

        }

        Write-Host -Separator `t $jobID $jobOrganisation $jobName $o365JobLastState $o365JobCreationTime $o365JobEndTime $o365JobDuration $processed $transferred
    }

$o365Licenses = Get-VBOLicense
write-host "<<<veeam_o365licenses:sep(9)>>>"
foreach ($o365License in $o365Licenses)
    {
        $state = $o365License.Status
        $supportExpirationDate = $o365License.SupportExpirationDate
        $validity = $($supportExpirationDate - (Get-Date)).TotalSeconds -as [int]
        $usedNumber = $o365License.UsedNumber
        $totalNumber = $o365License.TotalNumber
        Write-Host -Separator `t $state $supportExpirationDate $validity $usedNumber $totalNumber
    }
}
catch
{
$errMsg = $_.Exception.Message
$errItem = $_.Exception.ItemName
Write-Error "Totally unexpected and unhandled error occured:`n Item: $errItem`n Error Message: $errMsg"
Break
}
