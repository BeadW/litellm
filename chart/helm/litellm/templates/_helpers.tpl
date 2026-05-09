{{/*
Common naming + label helpers shared by gateway, backend, and ui templates.
*/}}

{{- define "litellm.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "litellm.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "litellm.gateway.fullname" -}}
{{- printf "%s-gateway" (include "litellm.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "litellm.backend.fullname" -}}
{{- printf "%s-backend" (include "litellm.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "litellm.ui.fullname" -}}
{{- printf "%s-ui" (include "litellm.fullname" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "litellm.commonLabels" -}}
app.kubernetes.io/name: {{ include "litellm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{- end -}}

{{/*
Per-component selector labels — used in both Service selectors and Deployment matchLabels.
*/}}
{{- define "litellm.gateway.selectorLabels" -}}
app.kubernetes.io/name: {{ include "litellm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: gateway
{{- end -}}

{{- define "litellm.backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "litellm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: backend
{{- end -}}

{{- define "litellm.ui.selectorLabels" -}}
app.kubernetes.io/name: {{ include "litellm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: ui
{{- end -}}

{{/*
Shared ServiceAccount name used by all three component Deployments. When
`serviceAccount.create` is true and `serviceAccount.name` is empty, default
to the chart fullname. When `create` is false, fall back to the provided
name or the namespace's `default` SA.
*/}}
{{- define "litellm.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{ default (include "litellm.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Master-key + database env block — gateway and backend share the same wiring.
*/}}
{{- define "litellm.serverEnv" -}}
- name: LITELLM_MASTER_KEY
  valueFrom:
    secretKeyRef:
      {{- if .Values.masterKey.existingSecret }}
      name: {{ .Values.masterKey.existingSecret }}
      {{- else }}
      name: {{ include "litellm.fullname" . }}-master-key
      {{- end }}
      key: master-key
{{- if .Values.database.existingSecret }}
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: {{ .Values.database.existingSecret }}
      key: {{ .Values.database.existingSecretKey }}
{{- else if .Values.database.url }}
- name: DATABASE_URL
  value: {{ .Values.database.url | quote }}
{{- end }}
{{- if .Values.redis.host }}
- name: REDIS_HOST
  value: {{ .Values.redis.host | quote }}
- name: REDIS_PORT
  value: {{ .Values.redis.port | quote }}
{{- if .Values.redis.existingSecret }}
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ .Values.redis.existingSecret }}
      key: {{ .Values.redis.existingSecretKey }}
{{- else if .Values.redis.password }}
- name: REDIS_PASSWORD
  value: {{ .Values.redis.password | quote }}
{{- end }}
{{- end }}
{{- with .Values.extraEnv }}
{{ toYaml . }}
{{- end }}
{{- end -}}
