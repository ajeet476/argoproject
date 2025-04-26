{{- define "argo-app.template.spec" -}}
{{- with .ArgoApp }}
project: {{ default "default" .project }}

destination:
  server: {{ .destination.server }}
{{- with .destination.namespace }}
  namespace: {{ . }}
{{- end }}

{{- include "argo-app.template.spec.sources" . | nindent 0 }}

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

{{- define "argo-app.template.spec.sources" -}}
{{- with .source }}
source:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- with .sources }}
sources:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}
