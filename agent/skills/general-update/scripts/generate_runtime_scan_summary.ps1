param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,
    [ValidateSet("normal", "history")]
    [string]$Mode = "normal",
    [switch]$ForceRefresh
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Strip-YamlScalar {
    param([string]$Value)

    if ($null -eq $Value) {
        return ""
    }

    $trimmed = $Value.Trim()
    if (
        ($trimmed.StartsWith("'") -and $trimmed.EndsWith("'")) -or
        ($trimmed.StartsWith('"') -and $trimmed.EndsWith('"'))
    ) {
        return $trimmed.Substring(1, $trimmed.Length - 2)
    }

    return $trimmed
}

function ConvertTo-Bool {
    param($Value)

    return [string]$Value -match '^(?i:true|yes|1)$'
}

function ConvertTo-IntOrDefault {
    param(
        $Value,
        [int]$DefaultValue
    )

    $parsed = 0
    if ([int]::TryParse([string]$Value, [ref]$parsed)) {
        return $parsed
    }

    return $DefaultValue
}

function Get-RelativePath {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    $baseUri = [System.Uri](((Resolve-Path $BasePath).Path.TrimEnd('\')) + '\')
    $targetUri = [System.Uri](Resolve-Path $TargetPath).Path
    return [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('\', '/')
}

function ConvertTo-UtcTimestamp {
    param([datetime]$Value)

    return $Value.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
}

function Parse-RuntimeScanConfig {
    param([string]$ManifestPath)

    if (-not (Test-Path $ManifestPath)) {
        throw "Missing project manifest: $ManifestPath"
    }

    $config = @{
        enabled = $false
        cache_relative_path = "00_GOVERNANCE/current_overview/runtime_scan_summary.json"
        refresh_after_hours = 24
        max_depth = 3
        include_sections = @()
        meaningful_extensions = @(".md", ".json")
        ignore_files = @("README.md", "project_manifest.yaml", "local_manifest.yaml", ".gitkeep")
        ignore_section_ids = @("99_ARCHIVE")
    }

    $insideBlock = $false
    $activeListKey = $null

    foreach ($line in Get-Content -LiteralPath $ManifestPath) {
        if (-not $insideBlock) {
            if ($line -match '^\s*runtime_scan:\s*$') {
                $insideBlock = $true
            }
            continue
        }

        if ($line -match '^\S') {
            break
        }

        if ($line -match '^\s{2}([a-zA-Z0-9_]+):\s*(.*?)\s*$') {
            $key = $matches[1]
            $rawValue = Strip-YamlScalar $matches[2]
            $activeListKey = $null

            if ($rawValue -eq "") {
                $config[$key] = @()
                $activeListKey = $key
            }
            else {
                $config[$key] = $rawValue
            }
            continue
        }

        if ($null -ne $activeListKey -and $line -match '^\s{4}-\s*(.*?)\s*$') {
            $config[$activeListKey] += Strip-YamlScalar $matches[1]
        }
    }

    $config.enabled = ConvertTo-Bool $config.enabled
    $config.refresh_after_hours = ConvertTo-IntOrDefault $config.refresh_after_hours 24
    $config.max_depth = ConvertTo-IntOrDefault $config.max_depth 3

    foreach ($listKey in @("include_sections", "meaningful_extensions", "ignore_files", "ignore_section_ids")) {
        if ($null -eq $config[$listKey]) {
            $config[$listKey] = @()
        }
        elseif ($config[$listKey] -isnot [System.Array]) {
            $config[$listKey] = @($config[$listKey])
        }
    }

    return $config
}

function Test-CacheIsFresh {
    param(
        [string]$CachePath,
        [int]$RefreshAfterHours,
        [string]$Mode
    )

    if (-not (Test-Path $CachePath)) {
        return $false
    }

    try {
        $cache = Get-Content -Raw -LiteralPath $CachePath | ConvertFrom-Json
        if ($cache.mode -ne $Mode) {
            return $false
        }

        $generatedAt = [datetime]::Parse(
            [string]$cache.generated_at,
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::AdjustToUniversal
        )
        $age = [datetime]::UtcNow - $generatedAt.ToUniversalTime()
        return $age.TotalHours -lt $RefreshAfterHours
    }
    catch {
        return $false
    }
}

function Get-MeaningfulFiles {
    param(
        [string]$SectionPath,
        [string[]]$MeaningfulExtensions,
        [string[]]$IgnoreFiles,
        [int]$MaxDepth
    )

    if (-not (Test-Path $SectionPath)) {
        return @()
    }

    $files = @()
    $resolvedSection = (Resolve-Path $SectionPath).Path

    foreach ($file in Get-ChildItem -LiteralPath $SectionPath -File -Recurse) {
        if ($IgnoreFiles -contains $file.Name) {
            continue
        }

        if ($MeaningfulExtensions -notcontains $file.Extension.ToLowerInvariant()) {
            continue
        }

        $relativePath = Get-RelativePath -BasePath $resolvedSection -TargetPath $file.FullName
        $depth = ($relativePath -split '/').Count
        if ($depth -gt $MaxDepth) {
            continue
        }

        $files += $file
    }

    return @($files)
}

function New-SectionSummary {
    param(
        [string]$ProjectRootResolved,
        [string]$SectionId,
        [hashtable]$Config
    )

    $sectionPath = Join-Path $ProjectRootResolved $SectionId
    $files = @(Get-MeaningfulFiles `
        -SectionPath $sectionPath `
        -MeaningfulExtensions $Config.meaningful_extensions `
        -IgnoreFiles $Config.ignore_files `
        -MaxDepth $Config.max_depth)

    if ($files.Count -eq 0) {
        return [pscustomobject]@{
            folder = $SectionId
            state = "default_empty"
            meaningful_file_count = 0
            latest_update = $null
        }
    }

    $latestUpdate = ($files | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1).LastWriteTimeUtc
    return [pscustomobject]@{
        folder = $SectionId
        state = "has_content"
        meaningful_file_count = $files.Count
        latest_update = ConvertTo-UtcTimestamp $latestUpdate
    }
}

$projectRootResolved = (Resolve-Path $ProjectRoot).Path
$manifestPath = Join-Path $projectRootResolved "project_manifest.yaml"
$config = Parse-RuntimeScanConfig -ManifestPath $manifestPath

if (-not $config.enabled) {
    throw "Runtime scan is not enabled in $manifestPath"
}

$cachePath = Join-Path $projectRootResolved $config.cache_relative_path.Replace('/', '\')

if ((-not $ForceRefresh) -and (Test-CacheIsFresh -CachePath $cachePath -RefreshAfterHours $config.refresh_after_hours -Mode $Mode)) {
    Get-Content -Raw -LiteralPath $cachePath
    return
}

$includeSections = @($config.include_sections)
if ($Mode -ne "history") {
    $includeSections = @($includeSections | Where-Object { $config.ignore_section_ids -notcontains $_ })
}

$sections = foreach ($sectionId in $includeSections) {
    New-SectionSummary -ProjectRootResolved $projectRootResolved -SectionId $sectionId -Config $config
}

$payload = [pscustomobject]@{
    generated_at = ConvertTo-UtcTimestamp ([datetime]::UtcNow)
    cache_path = $config.cache_relative_path.Replace('\', '/')
    refresh_after_hours = $config.refresh_after_hours
    max_depth = $config.max_depth
    mode = $Mode
    sections = [object[]]$sections
}

$cacheDirectory = Split-Path -Parent $cachePath
if (-not (Test-Path $cacheDirectory)) {
    New-Item -ItemType Directory -Path $cacheDirectory | Out-Null
}

$json = $payload | ConvertTo-Json -Depth 6
Set-Content -LiteralPath $cachePath -Value ($json + "`n") -Encoding UTF8
Write-Output $json
