import axios from "axios";

const API_URL = "http://localhost:8000";

export async function getLeaderboard(dataset) {
    
    const response = await axios.get(
        `${API_URL}/leaderboard/${dataset}`
    );

    return response.data;
}