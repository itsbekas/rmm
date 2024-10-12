export interface DeviceStatus {
    label: string;
    status: "run" | "pause" | "stop";
    completionTime: string;
    healthStatus: "ONLINE" | "OFFLINE";
    healthUpdated: string;
}

export interface StatusData {
    washers: DeviceStatus[];
    dryers: DeviceStatus[];
}