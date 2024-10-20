import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '~/components/ui/card';
import { Separator } from '~/components/ui/separator';
import { DeviceStatus } from './types';
import dayjs from 'dayjs';
import timezone from 'dayjs/plugin/timezone';
import utc from 'dayjs/plugin/utc';
import relativeTime from 'dayjs/plugin/relativeTime';
// import updateLocale from 'dayjs/plugin/updateLocale';

dayjs.extend(timezone);
dayjs.extend(utc);
dayjs.extend(relativeTime);
// dayjs.extend(updateLocale);
dayjs.tz.setDefault('Europe/Lisbon');
// dayjs.updateLocale('pt');


const OfflineCard: React.FC<{ device: DeviceStatus }> = ({ device }) => (
  <>
    <h3 className="text-xl font-bold">{device.label}</h3>
    <p className="text-red-600">Sem conexão</p>
  </>
);

const DeviceCard: React.FC<{ device: DeviceStatus }> = ({ device }) => (
  <>
    <h3 className="text-xl font-bold">{device.label}</h3>
    {device.state === 'run' ? (
      <p className="text-yellow-600">A lavar/secar</p>
    ) : (
      <p className="text-green-600">Vazia/Terminada</p>
    )}
    {/* <p>Completion Time: {dayjs(completionTime).format('MMMM D, YYYY h:mm A')}</p> */}
    {device.state === 'run' && (
      <p>Tempo restante: {dayjs(device.completionTime).fromNow(true)}</p>
    )}
    {!device.online && 
      <>
        <p className="text-xs"><span className="text-red-600">Sem conexão</span> - Última atualização: {dayjs(device.lastSeen).fromNow()}</p>
      </>
    }
  </>
);


export const DeviceStatusCard: React.FC<{ title: string, devices: DeviceStatus[] }> = ({ title, devices }) => {

  return (
    <Card>
      <CardHeader>
        <CardTitle className="scroll-m-20 text-2xl font-semibold tracking-tight min-w-80">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {devices.map((device, index) => (
          <div key={index}>
            <div className="mb-4">
              <DeviceCard device={device} />
            </div>
            {/* Separator between each device except the last one */}
            {index < devices.length - 1 && <Separator className="my-4" />}
          </div>
        ))}
      </CardContent>
    </Card>
  );
};
