import { getAccessToken } from "../utils/auth.js";

export const BASE_URL = "http://localhost:8000";

export function getAuthHeaders(){
    const token = getAccessToken();

    return {
        "Content-type": "application/json", 
    ...(token && {Authorization: `Bearer ${token}`})
    }
}