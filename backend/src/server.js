const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../.env") });

const express = require("express");
const cors = require("cors");
const apiRouter = require("./routes");
const mockRoutes = require("./routes/mock");
const thingSpeakRoutes = require("./routes/thingspeak");
const authRoutes = require("./routes/auth");
const { startThingSpeakPolling } = require("./services/thingspeakService");

const app = express();
const allowedOrigins = (process.env.CORS_ALLOWED_ORIGINS || "http://localhost:5173")
  .split(",").map(value => value.trim()).filter(Boolean);

app.disable("x-powered-by");
app.use((req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  next();
});
app.use(cors({ origin(origin, callback) {
  if (!origin || allowedOrigins.includes(origin)) return callback(null, true);
  return callback(new Error("Origin not allowed"));
}, credentials: false }));
app.use(express.json({ limit: process.env.JSON_BODY_LIMIT || "1mb" }));

function fixedWindowRateLimit({ windowMs, limit }) {
  const clients = new Map();
  return (req, res, next) => {
    const now = Date.now(); const key = req.ip; const current = clients.get(key);
    if (!current || current.resetAt <= now) clients.set(key, { count: 1, resetAt: now + windowMs });
    else if (++current.count > limit) {
      res.setHeader("Retry-After", Math.ceil((current.resetAt - now) / 1000));
      return res.status(429).json({ success: false, message: "Too many requests" });
    }
    return next();
  };
}

const authLimit = fixedWindowRateLimit({ windowMs: 15 * 60 * 1000, limit: 20 });
app.use(["/api/login", "/api/register", "/api/refresh-token"], authLimit);

app.get("/", (req, res) => res.send("Backend is running"));
app.get("/health", (req, res) => res.status(200).json({ status: "ok", timestamp: new Date().toISOString(), uptimeSeconds: process.uptime() }));
app.use("/api", apiRouter);
app.use("/api", authRoutes);
app.use("/api", mockRoutes);
app.use("/api", thingSpeakRoutes);
app.use((err, req, res, next) => { console.error("Unhandled request error", { message: err.message }); res.status(500).json({ success: false, message: "Request failed" }); });

const PORT = Number(process.env.PORT || 3000);
app.listen(PORT, () => { console.log(`Server listening on port ${PORT}`); startThingSpeakPolling(); });
