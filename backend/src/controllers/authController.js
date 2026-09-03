const authService = require("../services/authService");

function clientError(res, status, message) {
  return res.status(status).json({ success: false, message });
}

async function register(req, res) {
  try {
    const { username, password } = req.body;
    if (typeof username !== "string" || typeof password !== "string") {
      return clientError(res, 400, "Username and password are required");
    }
    if (username.trim().length < 3 || username.trim().length > 64 || password.length < 12) {
      return clientError(res, 400, "Username or password does not meet the security requirements");
    }
    const user = await authService.registerUser(username.trim(), password);
    return res.status(201).json({ success: true, message: "User registered successfully", user });
  } catch (error) {
    console.error("Registration failed", { message: error.message });
    return clientError(res, 400, "Unable to register user");
  }
}

async function login(req, res) {
  try {
    const { username, password } = req.body;
    if (typeof username !== "string" || typeof password !== "string") {
      return clientError(res, 400, "Username and password are required");
    }
    const result = await authService.loginUser(username.trim(), password);
    return res.status(200).json({ success: true, ...result });
  } catch (error) {
    console.warn("Login failed", { message: error.message });
    return clientError(res, 401, "Invalid username or password");
  }
}

function refreshToken(req, res) {
  try {
    const result = authService.refreshAccessToken(req.body.refreshToken);
    return res.status(200).json({ success: true, ...result });
  } catch (error) {
    console.warn("Token refresh failed", { message: error.message });
    return clientError(res, 403, "Invalid or expired refresh token");
  }
}

function logout(req, res) {
  try {
    const result = authService.logoutUser(req.body.refreshToken);
    return res.status(200).json({ success: true, ...result });
  } catch (error) {
    console.warn("Logout failed", { message: error.message });
    return clientError(res, 400, "Unable to log out");
  }
}

function getUsers(req, res) {
  try {
    return res.status(200).json({ success: true, message: "Users retrieved successfully", users: authService.getAllUsers() });
  } catch (error) {
    console.error("User listing failed", { message: error.message });
    return clientError(res, 500, "Unable to retrieve users");
  }
}

module.exports = { register, login, refreshToken, logout, getUsers };
