import streamlit as st
import requests

PROMETHEUS_URL = "http://prometheus:9090"

def prometheus_query(query: str):
    res = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
    try:
        return res.json()["data"]["result"]
    except:
        return []

st.title("🛡️ API Gateway Admin Dashboard")

# Total requests
total_requests = prometheus_query("sum(http_requests_total)")
st.metric("📦 Total Requests", total_requests[0]["value"][1] if total_requests else "N/A")

# 429 Errors
rate_limited = prometheus_query("sum(http_requests_total{status='429'})")
st.metric("⛔ Rate Limit Hits", rate_limited[0]["value"][1] if rate_limited else "0")

# Latency
latency = prometheus_query("rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])")
st.metric("⚡ Avg Latency (s)", f"{float(latency[0]['value'][1]):.3f}" if latency else "N/A")

try:
    mock_res = requests.get("http://mock_service:8001/status", timeout=2)
    st.success("🟢 Mock Service is UP")
except:
    st.error("🔴 Mock Service is DOWN")

st.subheader("⚙️ Restart Services via API Gateway")

if st.button("🔁 Restart Mock Service"):
    try:
        headers = {
            "Authorization": "Bearer test345",
            "Content-Type": "application/json"
        }

        payload = {
            "service_name": "mock_service"
        }

        res = requests.post(
            "http://gateway:8080/admin/restart_service",
            json=payload,
            headers=headers,
            timeout=5
        )

        if res.status_code == 200:
            result_json = res.json()
            if result_json.get("status") == "success":
                st.success(f"✅ Restarted: {result_json.get('output')}")
            else:
                st.error(f"❌ Failed: {result_json.get('output')}")
        else:
            st.error(f"❌ HTTP {res.status_code}: {res.text}")

    except Exception as e:
        st.error(f"🚨 Request failed: {e}")

