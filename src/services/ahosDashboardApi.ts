import axios from "axios";
import { getToken } from "../lib/auth-storage";

const API = "http://127.0.0.1:8000";

export const getUnifiedDashboardOverview = async () =>
  (await axios.get(`${API}/api/dashboard/overview`, {
    headers: getToken()
      ? { Authorization: `Bearer ${getToken()}` }
      : {},
  })).data;

export const getEventStore = async () =>
  getUnifiedDashboardOverview();

export const getSafety = async () =>
  getUnifiedDashboardOverview();

export const getCommandCenter = async () =>
  getUnifiedDashboardOverview();

export const getCDSS = async () =>
  getUnifiedDashboardOverview();

export const getCopilot = async () =>
  getUnifiedDashboardOverview();
