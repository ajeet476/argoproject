{{- define "app.istio.route.destination" -}}
{{- with .RouteDest }}
- destination:
    host: {{ .host }}
    subset: stable
  weight: 100
- destination:
    host: {{ .host }}
    subset: canary
  weight: 0
{{- end }}
{{- end }}

