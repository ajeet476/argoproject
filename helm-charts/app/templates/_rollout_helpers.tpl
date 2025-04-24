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
{{- with .Values.rollout }}
{{- $service := (include "app.fullname" . | trim) -}}
{{- if eq "canary" .type }}
canary:
  trafficRouting:
  {{- $istioVs := ("app.rollout.trafficRouting.istio" | fromYaml) -}}
  {{- if $istioVs }}
    istio:
      virtualServices:
      {{ toYaml $istioVs | nindent 8 }}
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
{{- else }}

{{- end }}
{{- end }}
