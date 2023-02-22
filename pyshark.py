import pyshark

class PacketAnalyzer:
    def __init__(self, interface):
        self.capture = pyshark.LiveCapture(interface=interface)
        self.capture.sniff(timeout=10)
        self.results = {}

    def analyze(self):
        for packet in self.capture:
            try:
                src = packet.ip.src
                dst = packet.ip.dst
                if packet.http:
                    url = packet.http.request_full_uri
                    if 'password' in url.lower() or 'login' in url.lower():
                        if src not in self.results:
                            self.results[src] = []
                        self.results[src].append({'url': url, 'dst': dst})
            except AttributeError:
                pass
        return self.results

if __name__ == '__main__':
    analyzer = PacketAnalyzer('en0')
    results = analyzer.analyze()
    print(results)
