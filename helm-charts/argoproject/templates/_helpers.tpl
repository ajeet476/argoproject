{{- define "argo-app.template.spec" -}}
{{- with .ArgoApp }}
project: {{ default "default" .project }}

source:
  repoURL: {{ .repoURL }}
  targetRevision: {{ .targetRevision }}
{{- with .helm }}
 {{- if .valueFiles }}
  valueFiles:
    {{- toYaml .valueFiles | nindent 4 }}
  {{- end }}
  {{- if .valuesObject }}
  valuesObject:
    {{- toYaml .valuesObject | nindent 4 }}
  {{- end }}
{{- end }}

destination:
  server: {{ .server }}
{{- with .namespace }}
  namespace: {{ . }}
{{- end }}

syncPolicy:
  automated:
    selfHeal: true
  syncOptions:
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    - ApplyOutOfSyncOnly=true
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m

{{- with .ignoreDifferences }}
ignoreDifferences:
  {{ . | nindent 2 }}
{{- end }}
{{- end }}
{{- end }}
