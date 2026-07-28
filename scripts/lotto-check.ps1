param(
  [Parameter(Position = 0)]
  [string]$FirstSet,

  [Parameter(Position = 1)]
  [string]$SecondSet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Parse-LottoNumbers {
  param(
    [Parameter(Mandatory = $true)]
    [string]$InputText,

    [Parameter(Mandatory = $true)]
    [string]$Name
  )

  if ([string]::IsNullOrWhiteSpace($InputText)) {
    throw "${Name}: enter 6 numbers separated by commas."
  }

  $parts = $InputText -split ','
  $numbers = @()

  foreach ($part in $parts) {
    $valueText = $part.Trim()

    if ($valueText -eq '') {
      throw "${Name}: empty item found. Use the format `"1, 2, 3, 4, 5, 6`"."
    }

    [int]$number = 0
    if (-not [int]::TryParse($valueText, [ref]$number)) {
      throw "${Name}: value '$valueText' is not an integer."
    }

    $numbers += $number
  }

  if ($numbers.Count -ne 6) {
    throw "${Name}: the set must contain exactly 6 numbers, got $($numbers.Count)."
  }

  $outOfRange = @($numbers | Where-Object { $_ -lt 1 -or $_ -gt 49 })
  if ($outOfRange.Count -gt 0) {
    throw "${Name}: numbers outside the 1-49 range: $($outOfRange -join ', ')."
  }

  $duplicates = @(
    $numbers |
      Group-Object |
      Where-Object { $_.Count -gt 1 } |
      ForEach-Object { $_.Name }
  )
  if ($duplicates.Count -gt 0) {
    throw "${Name}: duplicate numbers: $($duplicates -join ', ')."
  }

  return $numbers
}

try {
  if ([string]::IsNullOrWhiteSpace($FirstSet)) {
    $FirstSet = Read-Host 'Enter the first set (for example: 1, 2, 3, 4, 5, 6)'
  }

  if ([string]::IsNullOrWhiteSpace($SecondSet)) {
    $SecondSet = Read-Host 'Enter the second set (for example: 1, 8, 3, 10, 5, 12)'
  }

  $firstNumbers = Parse-LottoNumbers -InputText $FirstSet -Name 'First set'
  $secondNumbers = Parse-LottoNumbers -InputText $SecondSet -Name 'Second set'

  $firstNumberSet = [System.Collections.Generic.HashSet[int]]::new()
  foreach ($number in $firstNumbers) {
    [void]$firstNumberSet.Add($number)
  }

  $matches = 0
  foreach ($number in $secondNumbers) {
    if ($firstNumberSet.Contains($number)) {
      $matches++
    }
  }

  Write-Output $matches
}
catch {
  [Console]::Error.WriteLine($_.Exception.Message)
  exit 1
}
