const BACKEND_URL = "http://127.0.0.1:5001/latest";

async function fetchData() {
    try {
        const res = await fetch(BACKEND_URL);
        const data = await res.json();

        if (data.status) return;

        document.getElementById("latency").innerText =
            `Latency: ${data.latency_ms} ms`;

        document.getElementById("loss").innerText =
            `Packet Loss: ${data.packet_loss} %`;

        document.getElementById("users").innerText =
            `Active Users: ${data.active_users}`;

        document.getElementById("decision").innerText =
            JSON.stringify(data, null, 2);

    } catch (err) {
        console.error("Backend unreachable");
    }
}

setInterval(fetchData, 2000);
