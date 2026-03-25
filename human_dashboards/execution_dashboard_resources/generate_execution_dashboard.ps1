param(
    [string]$WorkspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$OutputHtmlPath = (Join-Path $PSScriptRoot "execution_items_kanban.html")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Web.Extensions

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

function Normalize-ExecutionStatus {
    param([string]$Value)

    $normalized = Normalize-Token $Value
    switch ($normalized) {
        "at_risk" { return "blocked" }
        "overdue" { return "blocked" }
        "abandoned" { return "abandonned" }
        "cancelled" { return "abandonned" }
        "canceled" { return "abandonned" }
        default { return $normalized }
    }
}

function ConvertTo-List {
    param($Value)

    $list = New-Object System.Collections.ArrayList

    if ($null -eq $Value) {
        return $list
    }

    if ($Value -is [System.Array]) {
        foreach ($entry in $Value) {
            [void]$list.Add($entry)
        }
        return $list
    }

    [void]$list.Add($Value)
    return $list
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

function ConvertTo-JavaScriptLiteral {
    param($Value)

    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        $items = foreach ($item in $Value) {
            ConvertTo-JavaScriptLiteral $item
        }
        return "[" + ($items -join ",") + "]"
    }

    if ($null -eq $Value) {
        return "null"
    }

    if ($Value -is [string]) {
        return (ConvertTo-Json -Compress -InputObject $Value)
    }

    if ($Value -is [bool]) {
        return $Value.ToString().ToLowerInvariant()
    }

    if ($Value -is [ValueType]) {
        return (ConvertTo-Json -Compress -InputObject $Value)
    }

    if ($Value -is [System.Collections.IDictionary]) {
        $pairs = foreach ($key in $Value.Keys) {
            $encodedKey = ConvertTo-Json -Compress -InputObject ([string]$key)
            $encodedValue = ConvertTo-JavaScriptLiteral $Value[$key]
            "${encodedKey}:$encodedValue"
        }
        return "{" + ($pairs -join ",") + "}"
    }

    $properties = $Value.PSObject.Properties | Where-Object { $_.MemberType -eq "NoteProperty" }
    if ($properties.Count -gt 0) {
        $pairs = foreach ($property in $properties) {
            $encodedKey = ConvertTo-Json -Compress -InputObject $property.Name
            $encodedValue = ConvertTo-JavaScriptLiteral $property.Value
            "${encodedKey}:$encodedValue"
        }
        return "{" + ($pairs -join ",") + "}"
    }

    return (ConvertTo-Json -Compress -InputObject ([string]$Value))
}

function Get-WorkspaceRelativePath {
    param(
        [string]$WorkspaceRoot,
        [string]$TargetPath
    )

    $workspaceResolved = (Resolve-Path $WorkspaceRoot).Path.TrimEnd('\')
    $targetResolved = (Resolve-Path $TargetPath).Path

    if ($targetResolved.StartsWith($workspaceResolved, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $targetResolved.Substring($workspaceResolved.Length).TrimStart('\').Replace('\', '/')
    }

    $baseUri = [System.Uri]($workspaceResolved + '\')
    $targetUri = [System.Uri]$targetResolved
    $relativeUri = $baseUri.MakeRelativeUri($targetUri)
    return [System.Uri]::UnescapeDataString($relativeUri.ToString()).Replace('\', '/')
}

function Convert-ToDisplayLabel {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }

    $label = $Value -replace '[_-]+', ' '
    return (Get-Culture).TextInfo.ToTitleCase($label.ToLowerInvariant())
}

function Get-DocumentPreview {
    param(
        [string]$Format,
        [string]$RawContent
    )

    if ([string]::IsNullOrWhiteSpace($RawContent)) {
        return ""
    }

    $candidate = ""

    if ($Format -eq "markdown") {
        $lines = @(
            ($RawContent -split "`r?`n") |
            ForEach-Object { $_.Trim() } |
            Where-Object { $_ -and -not $_.StartsWith("#") -and -not $_.StartsWith("- ") -and -not $_.StartsWith("* ") -and -not $_.StartsWith('```') }
        )

        if ($lines.Count -gt 0) {
            $candidate = [string]$lines[0]
        }
    }

    if ([string]::IsNullOrWhiteSpace($candidate)) {
        $candidate = (($RawContent -replace '\s+', ' ').Trim())
    }

    if ($candidate.Length -le 150) {
        return $candidate
    }

    return ($candidate.Substring(0, 147) + '...')
}

function Get-PreferredContentFiles {
    param(
        [string]$DirectoryPath,
        [bool]$Recurse = $true
    )

    if (-not (Test-Path $DirectoryPath)) {
        return @()
    }

    $files = @(
        Get-ChildItem -Path $DirectoryPath -File -Recurse:$Recurse |
        Where-Object {
            $extension = $_.Extension.ToLowerInvariant()
            $isIngestionSummary = $extension -eq ".md" -and $_.BaseName.ToLowerInvariant().EndsWith("-ingestion-summary")
            $isRuntimeScanSummary = $_.Name -ieq "runtime_scan_summary.json"
            ($extension -eq ".md" -or $extension -eq ".json") -and
            -not $isIngestionSummary -and
            -not $isRuntimeScanSummary -and
            $_.Name -ne "README.md" -and
            $_.Name -ne "local_manifest.yaml" -and
            $_.Name -ne "project_manifest.yaml"
        }
    )

    if (-not $files) {
        return @()
    }

    $selected = @()
    foreach ($group in ($files | Group-Object DirectoryName)) {
        $selected += $group.Group
    }

    return @($selected | Sort-Object FullName)
}

function New-ExecutionItemRecord {
    param(
        [string]$ProjectId,
        [string]$ProjectName,
        [string]$RelativePath,
        $RawItem
    )

    $status = Normalize-ExecutionStatus $RawItem.status
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

function New-DocumentRecord {
    param(
        [string]$WorkspaceRoot,
        [string]$ProjectId,
        [string]$ProjectName,
        [string]$SectionKey,
        [System.IO.FileInfo]$File
    )

    $relativePath = Get-WorkspaceRelativePath -WorkspaceRoot $WorkspaceRoot -TargetPath $File.FullName
    $format = if ($File.Extension.ToLowerInvariant() -eq ".md") { "markdown" } else { "json" }
    $rawContent = [string](Get-Content -Raw -LiteralPath $File.FullName)
    $content = if ($format -eq "markdown") { $rawContent } else { $rawContent | ConvertFrom-Json }
    $sourceName = if ($File.Name -eq "README.md") { $File.Directory.Name } else { [System.IO.Path]::GetFileNameWithoutExtension($File.Name) }

    return [pscustomobject]@{
        id = ($ProjectId + "::" + $SectionKey + "::" + $relativePath.Replace('\', '/'))
        project_id = $ProjectId
        project_name = $ProjectName
        relative_path = $relativePath.Replace('\', '/')
        slug = $sourceName
        title = Convert-ToDisplayLabel $sourceName
        format = $format
        preview = Get-DocumentPreview -Format $format -RawContent $rawContent
        content = $content
    }
}

$statusOrder = @("planned", "in_progress", "blocked", "done", "backlog", "abandonned")
$validStatuses = @($statusOrder)
$validTypes = @("issue", "milestone")
$validPriorities = @("low", "medium", "high", "critical")
$documentSectionDefinitions = @(
    [pscustomobject]@{
        key = "current_overview"
        label = "Current Overview"
        description = "Latest project-state summaries and quick navigation context."
        relative_path = "00_GOVERNANCE\current_overview"
        recurse = $true
    },
    [pscustomobject]@{
        key = "project_risk_register"
        label = "Project Risk Register"
        description = "Project-level delivery risks, contingencies, and owners."
        relative_path = "07_PROJECT_EXECUTION\project_risk_register"
        recurse = $true
    },
    [pscustomobject]@{
        key = "foundation"
        label = "Foundation"
        description = "Project definition, stakeholders, assumptions, and success framing."
        relative_path = "01_PROJECT_FOUNDATION"
        recurse = $true
    },
    [pscustomobject]@{
        key = "requirements"
        label = "Requirements"
        description = "User, system, and subsystem requirements grouped for review."
        relative_path = "03_REQUIREMENTS"
        recurse = $true
    },
    [pscustomobject]@{
        key = "roadmap"
        label = "Roadmap"
        description = "Forward delivery plan and milestone trajectory."
        relative_path = "07_PROJECT_EXECUTION\roadmap"
        recurse = $true
    },
    [pscustomobject]@{
        key = "change_log"
        label = "Change Log"
        description = "Append-only governance change history."
        relative_path = "00_GOVERNANCE\change_log"
        recurse = $true
    }
)

$workspaceRootResolved = (Resolve-Path $WorkspaceRoot).Path
$projectsManifestPath = Join-Path $workspaceRootResolved "projects_manifest.yaml"
$templatePath = Join-Path $PSScriptRoot "execution_dashboard_template.html"

if (-not (Test-Path $templatePath)) {
    throw "Missing dashboard template: $templatePath"
}

$warnings = @()
$executionItems = @()
$workspaceSections = @()
$projects = Parse-ProjectsManifest -ManifestPath $projectsManifestPath

foreach ($project in $projects) {
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
        $relativePath = Get-WorkspaceRelativePath -WorkspaceRoot $workspaceRootResolved -TargetPath $itemPath
        $record = New-ExecutionItemRecord -ProjectId $project.id -ProjectName $project.name -RelativePath $relativePath -RawItem $rawItem

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

foreach ($sectionDefinition in $documentSectionDefinitions) {
    $documents = @()

    foreach ($project in $projects) {
        $projectRoot = Join-Path $workspaceRootResolved $project.path
        $sectionPath = Join-Path $projectRoot $sectionDefinition.relative_path

        foreach ($file in Get-PreferredContentFiles -DirectoryPath $sectionPath -Recurse $sectionDefinition.recurse) {
            $documents += New-DocumentRecord `
                -WorkspaceRoot $workspaceRootResolved `
                -ProjectId $project.id `
                -ProjectName $project.name `
                -SectionKey $sectionDefinition.key `
                -File $file
        }
    }

    $sortedDocuments =
        $documents |
        Sort-Object `
            @{ Expression = { $_.project_id } }, `
            @{ Expression = { $_.relative_path } }, `
            @{ Expression = { $_.title } }

    $workspaceSections += [pscustomobject]@{
        key = $sectionDefinition.key
        label = $sectionDefinition.label
        type = "documents"
        description = $sectionDefinition.description
        documents = [object[]]$sortedDocuments
    }
}

$workspaceSections = @(
    $workspaceSections[0],
    [pscustomobject]@{
        key = "execution_items"
        label = "Execution Items"
        type = "board"
        description = "Normalized cross-project execution board generated from execution-item JSON files."
        documents = @()
    },
    $workspaceSections[1],
    $workspaceSections[2],
    $workspaceSections[3],
    $workspaceSections[4],
    $workspaceSections[5]
)

$sortedItems =
    $executionItems |
    Sort-Object `
        @{ Expression = { [array]::IndexOf($statusOrder, $_.status) } }, `
        @{ Expression = { if ([string]::IsNullOrWhiteSpace($_.target_date)) { "9999-99-99" } else { $_.target_date } } }, `
        @{ Expression = { $_.project_id } }, `
        @{ Expression = { $_.id } }

$template = Get-Content -Raw $templatePath
$dashboardDataJson = ConvertTo-JavaScriptLiteral ([object[]]$sortedItems)
$warningsJson = ConvertTo-JavaScriptLiteral ([object[]]$warnings)
$workspaceSectionsJson = ConvertTo-JavaScriptLiteral ([object[]]$workspaceSections)
$generatedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm")

$renderedHtml = $template.Replace("__DASHBOARD_DATA__", $dashboardDataJson)
$renderedHtml = $renderedHtml.Replace("__DASHBOARD_WARNINGS__", $warningsJson)
$renderedHtml = $renderedHtml.Replace("__WORKSPACE_SECTIONS__", $workspaceSectionsJson)
$renderedHtml = $renderedHtml.Replace("__GENERATED_AT__", $generatedAt)
$renderedHtml = $renderedHtml.Replace("__WORKSPACE_NAME__", [System.IO.Path]::GetFileName($workspaceRootResolved))

$outputDirectory = Split-Path -Parent $OutputHtmlPath
if (-not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

Set-Content -Path $OutputHtmlPath -Value $renderedHtml -Encoding UTF8
Write-Output "Dashboard written to $OutputHtmlPath"
