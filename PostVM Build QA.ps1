#Below will give you Server configuration Details
$os = Get-WMIObject Win32_OperatingSystem
$Resources = Get-WMIObject Win32_ComputerSystem
$name = Get-WMIObject Win32_ComputerSystem
$timezone = Get-WmiObject win32_timezone
$Object = New-Object PSObject -Property @{
TimeZone = $timezone.Caption
ServerName = $name.Caption
OS = $os.Caption
"CPU(Cores)"  = $Resources.NumberOfLogicalProcessors
"RAM(GB)" = $Resources.TotalPhysicalMemory/1GB
}
Write-Host "**Server configuration Details**"
Write-Output $Object | Format-List -Property ServerName, OS, TimeZone, 'CPU(Cores)', 'RAM(GB)'
#Below will give you Drive Sizes Details 
Write-Host "**Drive Sizes Details**"
""
Get-WmiObject Win32_LogicalDisk | Format-Table -AutoSize DeviceId, @{n="Size";e={[math]::Round($_.Size/1GB,2)}}
#Below Will give you NIC card details 
Write-Host "**NIC card details**"
""
$nic = Get-WmiObject win32_networkadapterconfiguration -filter "ipenabled = 'True'" | Select-Object IPAddress, DefaultIPGateway, MACAddress
Write-Output $nic | Format-List
#Below will Give you the Static Persistent Route Table
Write-Host "**Static Persistent Route Table**"
""
Get-WmiObject Win32_IP4PersistedRouteTable | Format-Table -AutoSize @{N='Network Address'; E={$_.Name}},@{N='Netmask'; E={$_.Mask}},@{N='Gateway Address'; E={$_.NextHop}}
#Below will give you service status and its version . Just add service name if any services needs to be added in future
Write-Host "**Service Status and it's Version Details**"
""
$servicenames = @(  
                     "SysEDGE",
                     "NetBackup Client Service",
                     "Opsware Agent"
					 "TeleVault"
					#"Add New Service Here" 
                  )
foreach ($servicename in $servicenames)
{   
    If (($servicestatus = (Get-Service $servicename -EV +QA -ErrorAction SilentlyContinue).status) -ne $null)
    	{     
    Write-Output "$servicename Status : $servicestatus!"
    	}
    else
    	{
    write-Output "$servicename : Service Does not exist!"
    	}
}
$versionnames = @(  
                     "VMware Tools"
		     "Symantec EndPoint Protection"
		     #"Add New Service with Version Here"
                  )
foreach ($versionname in $versionnames)
{   
    If (($versionstatus = (Get-Service $versionname -EV +QA -ErrorAction SilentlyContinue).status) -ne $null)
    	{     
    $version = (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | where{$_.DisplayName -eq $versionname}).DisplayVersion
	Write-Output "$versionname Status : $versionstatus!`r`n$versionname version: $version"
    	}
    else
 	{
    write-Output "$versionname : Service Does not exist!"
	""
    	}
}
""
#verify AV signature file up to date and Group Name
$SEPgroupname = (Get-ItemProperty "HKLM:SOFTWARE\Wow6432Node\Symantec\Symantec Endpoint Protection\SMC\SYLINK\SyLink").CurrentGroup
$SEPstatus = (Get-ItemProperty "HKLM:SOFTWARE\Wow6432Node\Symantec\Symantec Endpoint Protection\SMC\SYLINK\SyLink").CurrentMode
Write-Host "**SEP Status & Group Name**"
If ($os.Caption -like "*2012*")
	{
	$2012SEPdef = (Get-ItemProperty 'HKLM:SOFTWARE\Wow6432Node\Symantec\Symantec Endpoint Protection\AV').PatternFileDate
	""
	Write-Output "SEP Definations date: $($2012SEPdef[0]+1970)/$($2012SEPdef[1]+1)/$($2012SEPdef[2]) `r`nSEP GroupName : $SEPgroupname "
	}       
else
	{
	$2008SEPdef = Get-ItemProperty 'HKLM:SOFTWARE\Wow6432Node\Symantec\Symantec Endpoint Protection\CurrentVersion\SharedDefs'
	$2008defdate = Get-ItemProperty $2008SEPdef.DEFWATCH_10
	""
	Write-Output "SEP Definations date: $($2008defdate.Name) and was last written on $($2008defdate.LastWriteTime) `r`nSEP GroupName : $SEPgroupname "
	}
if ($SEPstatus -eq "1")
	{
	Write-Output "SEP Cleint is connected to SEP Manager"
	""
	}
else
	{
	Write-Output "SEP Cleint is NOT connected to SEP Manager . Please login to Server and Check Manaually"
	""
	}
#Below will give you the latest Date of Server Patched
$Patch = Get-WmiObject Win32_quickfixengineering | Sort-Object -Property InstalledOn -Descending -ErrorAction SilentlyContinue | Select -First 2
Write-Host "**Latest Date of Server Patched**"
If (($PatchDate = $Patch[0].InstalledOn)-ne $null)
	{     
    	""
    	Write-Output "Last Windows Update was Installed on $PatchDate" 
	""
    	}
else
    	{
    	""    
    	Write-Output "Please login to server and Check Windows Updates Manually"
	""
    	}
#Below will give you if Server is Licensed or not
$License = Get-WmiObject SoftwareLicensingProduct | Where{$_.PartialProductKey -and $_.Name -like "*Windows*"}
Write-Host "**Windows Activation Status**"
If ($License.LicenseStatus -eq 1)
   	{
    	""     
    	Write-Output "License of $($name.Caption) Server is Activated" 
    	}
else
    	{
    	""
    	Write-Output "Please login to server and Check Activation Manually"
    }
"" ; ""
Write-Output $QA