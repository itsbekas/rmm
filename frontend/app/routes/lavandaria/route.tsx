// routes/status.jsx
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { StatusData } from "./types";
import { DeviceStatusCard } from "./status_card";

// Loader function to fetch data from the backend
export const loader = async () => {
  // Fetch data from the local endpoint
  const response = await fetch("http://localhost:8000/status");
  const data: StatusData = await response.json();

  // Return the data to the component
  return json(data);
};

export default function StatusPage() {
  // Access the data from the loader
  const statusData: StatusData = useLoaderData();

  return (
    <div>
      <DeviceStatusCard
        title={'Máquinas de Lavar'}
        devices={statusData.washers}
      />
      <DeviceStatusCard
        title={'Máquinas de Secar'}
        devices={statusData.dryers}
      />
    </div>
  );
}
