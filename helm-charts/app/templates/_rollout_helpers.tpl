{{- define "app.rollout.trafficRouting.istio" -}}
{{- if and .Values.istio.create .Values.istio.gateway.create }}
{{- $service := (include "app.fullname" . | trim) -}}
{{- with .Values.istio.gateway }}
- name: {{ $service }}
{{- end }}
- name: {{ $service }}-cluster
{{- end }}
{{- end }}

{{- define "app.rollout.strategy" -}}
{{- $service := (include "app.fullname" . | trim) -}}
{{- $istioVs := (include "app.rollout.trafficRouting.istio" . | trim) -}}
{{- with .Values.rollout }}
{{- if eq "canary" .type }}
canary:
  trafficRouting:
  {{- if $istioVs }}
    istio:
      virtualServices:
      {{- $istioVs | nindent 8 }}
      destinationRule:
        name: {{ $service }}
        canarySubsetName: canary
        stableSubsetName: stable
  {{- end }}
  steps:
  - setWeight: 30
  - pause: {duration: 30s}
  - setWeight: 60
  - pause: {duration: 30s}
  - setWeight: 100
  - pause: {duration: 10}
{{- end }}
{{- end }}
{{- end }}
