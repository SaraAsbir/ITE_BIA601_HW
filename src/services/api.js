const BASE_URL = "https://salam29.pythonanywhere.com";

export const ENDPOINTS = {
    ga: "/api/ga",
    ga_mi: "/api/ga_mi",
    ga_chi: "/api/ga_chi",
    ga_pca: "/api/ga_pca",
    ga_rfe: "/api/ga_rfe",
};

export async function uploadAndAnalyze(endpointKey, file) {
    const endpoint = ENDPOINTS[endpointKey];
    if (!endpoint) throw new Error("Endpoint غير معروف");

    const formData = new FormData();
    formData.append("file", file);

    let res;
    try {
        res = await fetch(`${BASE_URL}${endpoint}`, { 
            method: "POST", 
            body: formData 
        });
    } catch (err) {
        throw new Error("فشل الاتصال بالخادم");
    }

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`فشل الطلب (${res.status}): ${text || "تحقق من الخادم"}`);
    }

    return res.json();
}
