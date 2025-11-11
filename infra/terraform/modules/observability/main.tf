terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0"
    }
  }
}

# ========== Cloud Monitoring Dashboard ==========
resource "google_monitoring_dashboard" "gateway" {
  project = var.project_id
  dashboard_json = jsonencode({
    displayName = "Bob Gateway — Prod"
    mosaicLayout = {
      columns = 12
      tiles = [
        {
          width  = 6
          height = 4
          widget = {
            title = "Gateway P95 Latency (ms)"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"${var.service_name}\""
                    aggregation = {
                      perSeriesAligner   = "ALIGN_DELTA"
                      crossSeriesReducer = "REDUCE_PERCENTILE_95"
                      alignmentPeriod    = "60s"
                      groupByFields      = ["resource.service_name"]
                    }
                  }
                }
                plotType = "LINE"
              }]
              yAxis = {
                label = "Latency (ms)"
                scale = "LINEAR"
              }
              thresholds = [{
                value = 10000
                label = "SLO: 10s"
              }]
            }
          }
        },
        {
          xPos   = 6
          width  = 6
          height = 4
          widget = {
            title = "Gateway Error Rate (%)"
            xyChart = {
              dataSets = [
                {
                  timeSeriesQuery = {
                    timeSeriesFilter = {
                      filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"${var.service_name}\" metric.label.\"response_code_class\"=~\"5..\""
                      aggregation = {
                        perSeriesAligner   = "ALIGN_DELTA"
                        crossSeriesReducer = "REDUCE_SUM"
                        alignmentPeriod    = "60s"
                      }
                    }
                  }
                  plotType   = "LINE"
                  targetAxis = "Y1"
                },
                {
                  timeSeriesQuery = {
                    timeSeriesFilter = {
                      filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"${var.service_name}\""
                      aggregation = {
                        perSeriesAligner   = "ALIGN_DELTA"
                        crossSeriesReducer = "REDUCE_SUM"
                        alignmentPeriod    = "60s"
                      }
                    }
                  }
                  plotType   = "LINE"
                  targetAxis = "Y1"
                }
              ]
              yAxis = {
                label = "Requests"
                scale = "LINEAR"
              }
              thresholds = [{
                value = 0.05
                label = "SLO: 5%"
              }]
            }
          }
        },
        {
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "Request Count"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"${var.service_name}\""
                    aggregation = {
                      perSeriesAligner   = "ALIGN_RATE"
                      crossSeriesReducer = "REDUCE_SUM"
                      alignmentPeriod    = "60s"
                    }
                  }
                }
                plotType = "LINE"
              }]
              yAxis = {
                label = "Requests/sec"
                scale = "LINEAR"
              }
            }
          }
        },
        {
          xPos   = 6
          yPos   = 4
          width  = 6
          height = 4
          widget = {
            title = "Container Instance Count"
            xyChart = {
              dataSets = [{
                timeSeriesQuery = {
                  timeSeriesFilter = {
                    filter = "metric.type=\"run.googleapis.com/container/instance_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"${var.service_name}\""
                    aggregation = {
                      perSeriesAligner   = "ALIGN_MEAN"
                      crossSeriesReducer = "REDUCE_SUM"
                      alignmentPeriod    = "60s"
                    }
                  }
                }
                plotType = "LINE"
              }]
              yAxis = {
                label = "Instances"
                scale = "LINEAR"
              }
            }
          }
        }
      ]
    }
  })
}

# ========== Alert Policy: Latency P95 ==========
resource "google_monitoring_alert_policy" "latency_p95" {
  project      = var.project_id
  display_name = "Gateway P95 > 10s (5m)"
  combiner     = "OR"
  enabled      = true

  conditions {
    display_name = "Latency P95 exceeds 10 seconds"
    condition_monitoring_query_language {
      query = <<-EOT
        fetch cloud_run_revision
        | metric 'run.googleapis.com/request_latencies'
        | filter resource.service_name == '${var.service_name}'
        | group_by 5m, [value_request_latencies_percentile: percentile(value.request_latencies, 95)]
        | every 1m
        | condition value_request_latencies_percentile > 10000 'ms'
      EOT
      duration = "300s"
      trigger {
        count = 1
      }
    }
  }

  documentation {
    content = <<-EOT
      Gateway P95 latency exceeded 10 seconds for 5 minutes.

      SLO: P95 latency ≤ 10s over 7-day window

      Troubleshooting:
      1. Check Cloud Trace for slow requests
      2. Verify Reasoning Engine response times
      3. Check for cold starts or scaling issues
      4. Review recent deployments

      Rollback: make rollback
      Dashboard: See "Bob Gateway — Prod" in Cloud Monitoring
    EOT
    mime_type = "text/markdown"
  }

  notification_channels = []

  alert_strategy {
    auto_close = "604800s" # 7 days
  }
}

# ========== Alert Policy: Error Rate ==========
resource "google_monitoring_alert_policy" "error_rate" {
  project      = var.project_id
  display_name = "Gateway Error Rate > 5% (5m)"
  combiner     = "OR"
  enabled      = true

  conditions {
    display_name = "Error rate exceeds 5%"
    condition_monitoring_query_language {
      query = <<-EOT
        fetch cloud_run_revision
        | metric 'run.googleapis.com/request_count'
        | filter resource.service_name == '${var.service_name}'
        | align delta(1m)
        | every 1m
        | group_by [response_code_class],
            [value_request_count_aggregate: aggregate(value.request_count)]
        | condition val() > 0.05
      EOT
      duration = "300s"
      trigger {
        count = 1
      }
    }
  }

  documentation {
    content = <<-EOT
      Gateway error rate exceeded 5% for 5 minutes.

      SLO: Error rate ≤ 5% over 7-day window

      Troubleshooting:
      1. Check Cloud Logging for error messages
      2. Verify Reasoning Engine availability
      3. Check authentication and IAM roles
      4. Review recent configuration changes

      Rollback: make rollback
      Dashboard: See "Bob Gateway — Prod" in Cloud Monitoring
    EOT
    mime_type = "text/markdown"
  }

  notification_channels = []

  alert_strategy {
    auto_close = "604800s" # 7 days
  }
}

# ========== Budget ==========
resource "google_billing_budget" "monthly" {
  billing_account = var.billing_account
  display_name    = "Bob — Monthly Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(floor(var.budget_amount_usd))
    }
  }

  threshold_rules {
    threshold_percent = 0.80
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.00
    spend_basis       = "CURRENT_SPEND"
  }

  all_updates_rule {
    pubsub_topic           = null
    schema_version         = "1.0"
    disable_default_iam_recipients = false
  }
}
