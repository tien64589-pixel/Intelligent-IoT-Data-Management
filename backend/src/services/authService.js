const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const userRepository = require("../repositories/userRepository");

function requiredSecret(name) {
  const value = process.env[name];
  if (!value || value.length < 32) {
    throw new Error(`${name} must be configured with at least 32 characters`);
  }
  return value;
}

const JWT_SECRET = requiredSecret("JWT_SECRET");
const REFRESH_TOKEN_SECRET = requiredSecret("REFRESH_TOKEN_SECRET");

function generateAccessToken(user) {
  return jwt.sign({ id: user.id, username: user.username, role: user.role }, JWT_SECRET, {
    expiresIn: process.env.ACCESS_TOKEN_EXPIRY || "15m",
    issuer: "intelligent-iot-api",
    audience: "intelligent-iot-client"
  });
}

function generateRefreshToken(user) {
  return jwt.sign({ id: user.id, username: user.username, role: user.role }, REFRESH_TOKEN_SECRET, {
    expiresIn: process.env.REFRESH_TOKEN_EXPIRY || "7d",
    issuer: "intelligent-iot-api",
    audience: "intelligent-iot-client"
  });
}

async function registerUser(username, password) {
  if (userRepository.findUserByUsername(username)) throw new Error("Username already exists");
  const passwordHash = await bcrypt.hash(password, 12);
  const createdUser = userRepository.createUser({ username, password_hash: passwordHash, role: "user" });
  const { password_hash, refreshToken, ...safeUser } = createdUser;
  return safeUser;
}

async function loginUser(username, password) {
  const user = userRepository.findUserByUsername(username);
  if (!user || !(await bcrypt.compare(password, user.password_hash))) throw new Error("Invalid credentials");
  const accessToken = generateAccessToken(user);
  const refreshToken = generateRefreshToken(user);
  userRepository.updateUserById(user.id, { refreshToken });
  return { message: "Login successful", accessToken, refreshToken, user: { id: user.id, username: user.username, role: user.role } };
}

function refreshAccessToken(refreshToken) {
  if (!refreshToken) throw new Error("Refresh token is required");
  if (!userRepository.findUserByRefreshToken(refreshToken)) throw new Error("Invalid refresh token");
  const decoded = jwt.verify(refreshToken, REFRESH_TOKEN_SECRET, { issuer: "intelligent-iot-api", audience: "intelligent-iot-client" });
  return { message: "Access token refreshed successfully", accessToken: generateAccessToken(decoded) };
}

function logoutUser(refreshToken) {
  if (!refreshToken) throw new Error("Refresh token is required");
  const user = userRepository.findUserByRefreshToken(refreshToken);
  if (!user) throw new Error("Invalid refresh token");
  userRepository.updateUserById(user.id, { refreshToken: null });
  return { message: "Logout successful" };
}

function getAllUsers() { return userRepository.getSafeUsers(); }
module.exports = { registerUser, loginUser, refreshAccessToken, logoutUser, getAllUsers };
