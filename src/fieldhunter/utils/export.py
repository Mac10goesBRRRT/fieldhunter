"""Export raw inference results without consulting ground truth."""

import json
from pathlib import Path


def writeRawFields(filename, messages, inferredTypes, pcapfilename):
    """Write all candidates per imported message, before overlap resolution.

    Message indices are 1-based loader indices, not PCAP frame numbers.
    Field offsets are 0-based byte offsets into the TCP/UDP payload; ends
    are exclusive. Messages without inferred fields are included as well.
    """
    fieldsByMessage = {message: [] for message in messages}
    for inferred in inferredTypes:
        for segments in inferred.segments:
            for segment in segments:
                fieldsByMessage[segment.message].append({
                    "type": inferred.typelabel,
                    "offset": segment.offset,
                    "length": len(segment.bytes),
                    "end": segment.nextOffset,
                    "hex": segment.bytes.hex(),
                })

    records = []
    for index, message in enumerate(messages, start=1):
        records.append({
            "message_index": index,
            "message_id": str(message.id),
            "timestamp": float(message.date),
            "transport_protocol": message.l4Protocol,
            "source_ip": message.l3SourceAddress,
            "source_port": message.l4SourceAddress,
            "destination_ip": message.l3DestinationAddress,
            "destination_port": message.l4DestinationAddress,
            "payload_hex": message.data.hex(),
            "fields": sorted(fieldsByMessage[message],
                             key=lambda field: (field["offset"], field["type"], field["length"])),
        })

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as output:
        json.dump({
            "pcap": str(pcapfilename),
            "offset_reference": "transport_payload",
            "messages": records,
        }, output, indent=2)
        output.write("\n")
    print("Write raw inferred fields to", path)
