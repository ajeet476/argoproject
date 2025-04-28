{{- define "app.rollout.trafficRouting.istio" -}}
{{- if and .Values.istio.create .Values.istio.gateway.create }}
{{- $service := (include "app.fullname" . | trim) -}}
{{- with .Values.istio.gateway }}
- name: {{ $service }}
{{- end }}
- name: {{ $service }}-cluster
{{- end }}
{{- end }}

{{- define "app.rollout.background.analysis" }}
{{- with .analysisTemplate }}
{{- if or .errorLogs.enabled .successRate.enabled }}
analysis:
  templates:
{{- if .errorLogs.enabled }}
    - templateName: errorLogs
{{- end }}
{{- if .successRate.enabled }}
    - templateName: successRate
{{- end }}
  startingStep: 2 # delay starting analysis run until smoke test
{{- $args := concat .errorLogs.args .successRate.args | uniq }}
  args:
{{- toYaml $args | nindent 4 }}
{{- end }}
{{- end }}
{{- end }}

{{- define "app.rollout.smoketest.analysis" }}
{{- with .analysisTemplate }}
{{- if or .smokeTest.enabled }}
- setCanaryScale:
    replicas: 1
- setHeaderRoute: # enable header based traffic routing where
    name: "smoke-test-header"
    match:
    - headerName: smoke-test
      headerValue:
        exact: Mozilla
- analysis:
    templates:
       - templateName: smokeTest
    {{- with .errorLogs.args }}
    args:
    {{- toYaml . | nindent 6 }}
    {{- end }}
- setHeaderRoute:
    name: "smoke-test-header" # disable header based traffic routing
- setCanaryScale:
    matchTrafficWeight: true
{{- end }}
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
  {{- include "app.rollout.background.analysis" . | nindent 2 }}
  steps:
  {{- include "app.rollout.smoketest.analysis" . | nindent 2 }}
  - setWeight: 30
  - pause: {duration: 30s}
  - setWeight: 60
  - pause: {duration: 30s}
  - setWeight: 100
  - pause: {duration: 10}
{{- end }}
{{- end }}
{{- end }}
