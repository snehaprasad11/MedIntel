const csvPaths = {
  departments: "analytics/output/department_load.csv",
  hours: "analytics/output/hourly_traffic.csv",
  waits: "analytics/output/wait_time_trend.csv",
  weekends: "analytics/output/weekend_vs_weekday.csv",
};

const numberFormat = new Intl.NumberFormat("en-US");

async function loadCsv(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`Unable to load ${path}`);
  }

  const text = await response.text();
  const [headerLine, ...rows] = text.trim().split(/\r?\n/);
  const headers = headerLine.split(",");

  return rows.map((row) => {
    const values = row.split(",");
    return headers.reduce((record, header, index) => {
      const value = values[index];
      const numericValue = Number(value);
      record[header] = Number.isNaN(numericValue) ? value : numericValue;
      return record;
    }, {});
  });
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function renderBars(id, rows, labelKey, valueKey, labelPrefix = "") {
  const container = document.getElementById(id);
  if (!container) return;

  const max = Math.max(...rows.map((row) => row[valueKey]));
  container.innerHTML = rows
    .map((row) => {
      const pct = Math.max((row[valueKey] / max) * 100, 4);
      const label = `${labelPrefix}${row[labelKey]}`;
      return `
        <div class="bar-row">
          <span>${label}</span>
          <span class="bar-track"><span class="bar-fill" style="--value:${pct}%"></span></span>
          <span>${numberFormat.format(row[valueKey])}</span>
        </div>
      `;
    })
    .join("");
}

function renderLineChart(canvas, rows) {
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const cssWidth = canvas.clientWidth;
  const cssHeight = Math.max(260, Math.round(cssWidth * 0.3));

  canvas.width = Math.round(cssWidth * dpr);
  canvas.height = Math.round(cssHeight * dpr);
  ctx.scale(dpr, dpr);

  const values = rows.map((row) => row.avg_wait_time);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const pad = 34;
  const width = cssWidth - pad * 2;
  const height = cssHeight - pad * 2;

  ctx.clearRect(0, 0, cssWidth, cssHeight);
  ctx.strokeStyle = "#dfe6ef";
  ctx.lineWidth = 1;
  ctx.font = "12px system-ui";
  ctx.fillStyle = "#66758c";

  for (let i = 0; i <= 4; i += 1) {
    const y = pad + (height / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(cssWidth - pad, y);
    ctx.stroke();
  }

  ctx.beginPath();
  rows.forEach((row, index) => {
    const x = pad + (index / (rows.length - 1)) * width;
    const y = pad + (1 - (row.avg_wait_time - min) / (max - min || 1)) * height;
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.strokeStyle = "#146c94";
  ctx.lineWidth = 2.5;
  ctx.stroke();

  const avg = values.reduce((sum, value) => sum + value, 0) / values.length;
  const avgY = pad + (1 - (avg - min) / (max - min || 1)) * height;
  ctx.setLineDash([6, 6]);
  ctx.beginPath();
  ctx.moveTo(pad, avgY);
  ctx.lineTo(cssWidth - pad, avgY);
  ctx.strokeStyle = "#c77700";
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillText(`Avg ${avg.toFixed(1)} min`, pad + 8, avgY - 8);
}

async function init() {
  const [departments, hours, waits, weekends] = await Promise.all([
    loadCsv(csvPaths.departments),
    loadCsv(csvPaths.hours),
    loadCsv(csvPaths.waits),
    loadCsv(csvPaths.weekends),
  ]);

  const totalAppointments = departments.reduce((sum, row) => sum + row.total_appointments, 0);
  const avgWait = waits.reduce((sum, row) => sum + row.avg_wait_time, 0) / waits.length;
  const peakHour = [...hours].sort((a, b) => b.total_appointments - a.total_appointments)[0];
  const weekendRow = weekends.find((row) => String(row.day_type).toLowerCase() === "weekend");
  const weekendPct = weekendRow ? (weekendRow.total_appointments / totalAppointments) * 100 : 0;

  setText("appointmentsMetric", numberFormat.format(totalAppointments));
  setText("waitMetric", `${avgWait.toFixed(1)} min`);
  setText("hourMetric", `${peakHour.arrival_hour}:00`);
  setText("weekendMetric", `${weekendPct.toFixed(1)}%`);
  setText("trendRange", `${waits[0].date} to ${waits[waits.length - 1].date}`);

  renderBars("departmentBars", departments.slice(0, 8), "department_id", "total_appointments", "Dept ");
  renderBars("hourBars", hours, "arrival_hour", "total_appointments", "");

  const canvas = document.getElementById("waitChart");
  renderLineChart(canvas, waits);
  window.addEventListener("resize", () => renderLineChart(canvas, waits), { passive: true });
}

init().catch((error) => {
  console.error(error);
  setText("trendRange", "Unable to load analytics files");
});
