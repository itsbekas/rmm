export interface DeviceStatus {
    label: string;
    state: "run" | "pause" | "stop";
    completionTime: string;
    online: "ONLINE" | "OFFLINE";
    lastSeen: string;
}

export interface StatusData {
    washers: DeviceStatus[];
    dryers: DeviceStatus[];
}