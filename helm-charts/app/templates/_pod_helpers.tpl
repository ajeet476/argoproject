{{- define "app.pod.metadata" -}}
{{- with .Values.podAnnotations }}
annotations:
{{- toYaml . | nindent 2 }}
{{- end }}
labels:
{{- include "app.labels" . | nindent 2 }}
{{- with .Values.podLabels }}
{{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}

{{- define "app.pod.spec" -}}
{{- with .Values.imagePullSecrets }}
imagePullSecrets:
{{- toYaml . | nindent 2 }}
{{- end }}
serviceAccountName: {{ include "app.serviceAccountName" . }}
securityContext:
{{- toYaml .Values.podSecurityContext | nindent 2 }}
containers:
- name: {{ .Chart.Name }}
  securityContext:
    {{- toYaml .Values.securityContext | nindent 4 }}
  image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
  imagePullPolicy: {{ .Values.image.pullPolicy }}
  ports:
    - name: http
      containerPort: {{ .Values.service.port }}
      protocol: TCP
  livenessProbe:
    {{- toYaml .Values.livenessProbe | nindent 4 }}
  readinessProbe:
    {{- toYaml .Values.readinessProbe | nindent 4 }}
  resources:
    {{- include "app.resources" . | trim | nindent 4 }}
  {{- with .Values.volumeMounts }}
  volumeMounts:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- with .Values.volumes }}
volumes:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.nodeSelector }}
nodeSelector:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.affinity }}
affinity:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- with .Values.tolerations }}
tolerations:
{{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}
