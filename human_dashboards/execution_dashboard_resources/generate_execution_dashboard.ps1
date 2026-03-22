param(
    [string]$WorkspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$OutputHtmlPath = (Join-Path $PSScriptRoot "execution_items_kanban.html")
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

function Parse-ProjectsManifest {
    param([string]$ManifestPath)

    if (-not (Test-Path $ManifestPath)) {
        throw "Missing workspace projects manifest: $ManifestPath"
    }

    $projects = @()
    $current = $null

    foreach ($line in Get-Content $ManifestPath) {
        if ($line -match '^\s*-\s+id:\s*(.+?)\s*$') {
            if ($null -ne $current -and $current.path) {
                $projects += [pscustomobject]$current
            }

            $current = @{
                id = Strip-YamlScalar $matches[1]
                name = $null
                path = $null
            }
            continue
        }

        if ($null -eq $current) {
            continue
        }

        if ($line -match '^\s+name:\s*(.+?)\s*$') {
            $current.name = Strip-YamlScalar $matches[1]
            continue
        }

        if ($line -match '^\s+path:\s*(.+?)\s*$') {
            $current.path = Strip-YamlScalar $matches[1]
            continue
        }
    }

    if ($null -ne $current -and $current.path) {
        $projects += [pscustomobject]$current
    }

    return $projects
}

function Parse-ExecutionItemNames {
    param([string]$LocalManifestPath)

    if (-not (Test-Path $LocalManifestPath)) {
        return @()
    }

    $names = @()
    foreach ($line in Get-Content $LocalManifestPath) {
        if ($line -match '^\s*-\s+name:\s*(.+?)\s*$') {
            $name = Strip-YamlScalar $matches[1]
            if ($name.ToLowerInvariant().EndsWith(".json")) {
                $names += $name
            }
        }
    }

    return $names
}

function Normalize-Token {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }

    return ($Value.Trim().ToLowerInvariant() -replace '[\s-]+', '_')
}

function ConvertTo-List {
    param($Value)

    if ($null -eq $Value) {
        return @()
    }

    if ($Value -is [System.Array]) {
        return @($Value)
    }

    return @($Value)
}

function Get-OptionalPropertyValue {
    param(
        $Object,
        [string]$Name
    )

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return $null
    }

    return $property.Value
}

function New-ExecutionItemRecord {
    param(
        [string]$ProjectId,
        [string]$ProjectName,
        [string]$RelativePath,
        $RawItem
    )

    $status = Normalize-Token $RawItem.status
    $priority = Normalize-Token $RawItem.priority
    $type = Normalize-Token $RawItem.type

    return [pscustomobject]@{
        project_id = $ProjectId
        project_name = $ProjectName
        relative_path = $RelativePath.Replace('\', '/')
        id = [string]$RawItem.id
        type = $type
        title = [string]$RawItem.title
        status = $status
        owner = [string]$RawItem.owner
        created = [string]$RawItem.created
        target_date = [string]$RawItem.target_date
        completion_date = [string]$RawItem.completion_date
        priority = $priority
        summary = [string]$RawItem.summary
        dependencies = ConvertTo-List (Get-OptionalPropertyValue -Object $RawItem -Name "dependencies")
        linked_artifacts = ConvertTo-List (Get-OptionalPropertyValue -Object $RawItem -Name "linked_artifacts")
        notes = ConvertTo-List (Get-OptionalPropertyValue -Object $RawItem -Name "notes")
        problem_statement = [string](Get-OptionalPropertyValue -Object $RawItem -Name "problem_statement")
        definition_of_done = ConvertTo-List (Get-OptionalPropertyValue -Object $RawItem -Name "definition_of_done")
        deliverables = ConvertTo-List (Get-OptionalPropertyValue -Object $RawItem -Name "deliverables")
    }
}

$statusOrder = @("planned", "in_progress", "blocked", "done")
$validStatuses = @($statusOrder + @("cancelled"))
$validTypes = @("issue", "milestone")
$validPriorities = @("low", "medium", "high", "critical")

$workspaceRootResolved = (Resolve-Path $WorkspaceRoot).Path
$projectsManifestPath = Join-Path $workspaceRootResolved "projects_manifest.yaml"
$templatePath = Join-Path $PSScriptRoot "execution_dashboard_template.html"

if (-not (Test-Path $templatePath)) {
    throw "Missing dashboard template: $templatePath"
}

$warnings = @()
$executionItems = @()

foreach ($project in Parse-ProjectsManifest -ManifestPath $projectsManifestPath) {
    $projectRoot = Join-Path $workspaceRootResolved $project.path
    $executionItemDir = Join-Path $projectRoot "07_PROJECT_EXECUTION\execution_items"
    $localManifestPath = Join-Path $executionItemDir "local_manifest.yaml"

    if (-not (Test-Path $executionItemDir) -or -not (Test-Path $localManifestPath)) {
        continue
    }

    foreach ($itemName in Parse-ExecutionItemNames -LocalManifestPath $localManifestPath) {
        $itemPath = Join-Path $executionItemDir $itemName
        if (-not (Test-Path $itemPath)) {
            $warnings += "Missing execution item listed in manifest: $($project.id)/$itemName"
            continue
        }

        $rawItem = Get-Content -Raw $itemPath | ConvertFrom-Json
        $record = New-ExecutionItemRecord -ProjectId $project.id -ProjectName $project.name -RelativePath (Resolve-Path -Relative $itemPath) -RawItem $rawItem

        if ($validStatuses -notcontains $record.status) {
            $warnings += "Skipped $($record.id) because status '$($record.status)' is not normalized."
            continue
        }

        if ($validTypes -notcontains $record.type) {
            $warnings += "Skipped $($record.id) because type '$($record.type)' is not supported."
            continue
        }

        if ($record.priority -and ($validPriorities -notcontains $record.priority)) {
            $warnings += "Skipped $($record.id) because priority '$($record.priority)' is not normalized."
            continue
        }

        $executionItems += $record
    }
}

$sortedItems =
    $executionItems |
    Sort-Object `
        @{ Expression = { [array]::IndexOf($statusOrder, $_.status) } }, `
        @{ Expression = { if ([string]::IsNullOrWhiteSpace($_.target_date)) { "9999-99-99" } else { $_.target_date } } }, `
        @{ Expression = { $_.project_id } }, `
        @{ Expression = { $_.id } }

$template = Get-Content -Raw $templatePath
$dashboardDataJson = $sortedItems | ConvertTo-Json -Depth 8
$warningsJson = $warnings | ConvertTo-Json -Depth 4
$generatedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm")

$renderedHtml = $template.Replace("__DASHBOARD_DATA__", $dashboardDataJson)
$renderedHtml = $renderedHtml.Replace("__DASHBOARD_WARNINGS__", $warningsJson)
$renderedHtml = $renderedHtml.Replace("__GENERATED_AT__", $generatedAt)
$renderedHtml = $renderedHtml.Replace("__WORKSPACE_NAME__", [System.IO.Path]::GetFileName($workspaceRootResolved))

$outputDirectory = Split-Path -Parent $OutputHtmlPath
if (-not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

Set-Content -Path $OutputHtmlPath -Value $renderedHtml -Encoding UTF8
Write-Output "Dashboard written to $OutputHtmlPath"
