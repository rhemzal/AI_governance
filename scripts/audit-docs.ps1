Param(
  [switch]$FailOnWarning = $false
)

$ErrorActionPreference = 'Stop'

function Write-Result {
  Param(
    [string]$Level,
    [string]$Message
  )
  $prefix = "[$Level]"
  Write-Host "$prefix $Message"
}

$repoRoot = (Get-Location).Path
$mdFiles = Get-ChildItem -Recurse -File -Filter *.md

$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

# 1) Tabs in markdown (format drift / lint hazard)
foreach ($f in $mdFiles) {
  $raw = Get-Content $f.FullName -Raw
  if ($raw -match "\t") {
    $warnings.Add("Tabs found in: $($f.FullName.Substring($repoRoot.Length+1))")
  }
}

# 2) Backtick .md references must exist
$refRegex = [regex]'`([A-Za-z0-9_./-]+\.md)`'
foreach ($f in $mdFiles) {
  $raw = Get-Content $f.FullName -Raw
  $matches = $refRegex.Matches($raw)
  foreach ($m in $matches) {
    $p = $m.Groups[1].Value
    $target = Join-Path $repoRoot $p
    if (-not (Test-Path $target)) {
      $errors.Add("Missing referenced file: $($f.FullName.Substring($repoRoot.Length+1)) -> $p")
    }
  }
}

# 3) Required hub links (discoverability)
$readme = Join-Path $repoRoot 'README.md'
if (Test-Path $readme) {
  $r = Get-Content $readme -Raw
  if ($r -notmatch 'constitution/AI_RULES\.md') { $warnings.Add('README.md missing link/reference to constitution/AI_RULES.md') }
  if ($r -notmatch 'architecture/ARCHITECTURE_DECISION_FRAMEWORK\.md') { $warnings.Add('README.md missing link/reference to architecture/ARCHITECTURE_DECISION_FRAMEWORK.md') }
}

# 4) Terminology drift guard (normative docs)
# Prevent accidental reintroduction of hex-only phrasing in enforceable docs.
$normativeFolders = @('constitution', 'ci', 'interface')
$normativeFiles = foreach ($folder in $normativeFolders) {
  $p = Join-Path $repoRoot $folder
  if (Test-Path $p) {
    Get-ChildItem -Path $p -Recurse -File -Filter *.md
  }
}


# Keep patterns ASCII-only to avoid Windows PowerShell encoding pitfalls.
$forbiddenPhrases = @(
  'Hexagonal profile',
  'Ports & Adapters architecture',
  'Adapters -> Ports',
  'adapter bypasses ports',
  'bypassing ports',
  'ports mocked or faked'
)

foreach ($f in $normativeFiles) {
  $raw = Get-Content $f.FullName -Raw
  foreach ($phrase in $forbiddenPhrases) {
    if ($raw -match [regex]::Escape($phrase)) {
      $warnings.Add("Terminology drift (normative): $($f.FullName.Substring($repoRoot.Length+1)) contains '$phrase'")
    }
  }
}

# Print
foreach ($e in $errors) { Write-Result -Level 'ERROR' -Message $e }
foreach ($w in $warnings) { Write-Result -Level 'WARN' -Message $w }

if ($errors.Count -gt 0) {
  Write-Result -Level 'FAIL' -Message ("Doc audit failed with {0} error(s)." -f $errors.Count)
  exit 2
}

if ($FailOnWarning -and $warnings.Count -gt 0) {
  Write-Result -Level 'FAIL' -Message ("Doc audit failed with {0} warning(s) (FailOnWarning)." -f $warnings.Count)
  exit 3
}

Write-Result -Level 'OK' -Message ("Doc audit passed ({0} warning(s))." -f $warnings.Count)
exit 0
